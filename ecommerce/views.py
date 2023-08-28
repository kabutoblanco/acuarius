from django.views.generic import ListView, DetailView, CreateView
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _
from django.db.models import F, Sum, Value
from django.conf import settings

import uuid
import json
from datetime import datetime, timedelta

from .forms import OrderForm, PaymentForm
from .models import Customer, Product, CartProduct, Payment, Order, OrderProduct, Banner

from .services import get_token_epayco, payment_pse, get_banks as get_banks_api, get_client_ip


PRICE_SENDING = 5000


# Create your views here.
class MainListView(ListView):
    context_object_name = 'product_list'
    template_name = 'home.html'
    queryset = Product.objects.filter(type_product=1)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        queryset_banner = Banner.objects.all()

        context['banners'] = queryset_banner

        return context


class CategoryListView(ListView):
    context_object_name = 'product_list'
    template_name = 'category.html'

    def get_queryset(self):
        category = self.kwargs['category']
        queryset = Product.objects.filter(categories__path=category)
        return queryset


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product-detail.html'

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        context = super().get_context_data(**kwargs)

        queryset_product = Product.objects.get(id=pk)
        queryset_details = Product.objects.filter(type_product=2)

        context['product'] = queryset_product
        context['details'] = queryset_details

        return context

    def post(self, request, *args, **kwargs):
        product = Product.objects.get(id=kwargs['pk'])
        details = self.request.POST['details'].split(",")
        device = request.COOKIES.get('sessionid', '')
        customer, created = Customer.objects.get_or_create(uid_device=device)
        cart_product = CartProduct(customer=customer, product=product, amount=self.request.POST['amount'], color=self.request.POST['color'], note=self.request.POST['note'])
        cart_product.save()

        for detail in details:
            if detail != '':
                product = Product.objects.get(id=detail)
                cart_product = CartProduct(customer=customer, product=product, amount=1)
                cart_product.save()

        return redirect('/carrito')


class CartView(ListView):
    context_object_name = 'product_list'
    template_name = 'cart.html'

    def get_queryset(self):
        device = self.request.COOKIES.get('sessionid', '')
        queryset = CartProduct.objects.filter(customer__uid_device=device)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        details = queryset \
                    .annotate(discount=F('product__price') * F('product__discount') * F('amount'), total=F('product__price') * F('amount')) \
                    .aggregate(Sum('discount', default=Value(0)), Sum('total', default=Value(0)))

        context['discount'] = details['discount__sum']
        context['subtotal'] = details['total__sum']
        context['total'] = details['total__sum'] - details['discount__sum']
        return context

    def post(self, request, *args, **kwargs):
        return redirect('/orden')


def update_cart(request, pk, type):
    factor = 1 if type else -1
    device = request.COOKIES.get('sessionid', '')
    cart_product = CartProduct.objects.get(id=pk)

    if type == 2:
        cart_product.delete()
    else:
        cart_product.amount += factor
        cart_product.save()

    queryset = CartProduct.objects.filter(customer__uid_device=device)
    details = queryset \
                .annotate(discount=F('product__price') * F('product__discount') * F('amount'), total=F('product__price') * F('amount')) \
                .aggregate(Sum('discount', default=Value(0)), Sum('total', default=Value(0)))
    
    details.update({'total_self': cart_product.get_total, 'type': type})
    return JsonResponse(details)


def get_banks(request):
    token = get_token_epayco()
    payment_response = get_banks_api(token)
    return JsonResponse(payment_response)


def update_order(request):
    device = request.COOKIES.get('sessionid', '')

    queryset = CartProduct.objects.filter(customer__uid_device=device)
    details = queryset \
                .annotate(discount=F('product__price') * F('product__discount') * F('amount'), total=F('product__price') * F('amount')) \
                .aggregate(Sum('discount', default=Value(0)), Sum('total', default=Value(0)))

    json_data = json.loads(request.body)
    price_sending = 0 if json_data['isPickup'] else PRICE_SENDING

    details['price_sending'] = price_sending
    details['total'] = details['total__sum'] - details['discount__sum'] + price_sending
    return JsonResponse(details)


class OrderView(CreateView):
    model = Order
    template_name = 'order.html'
    form_class = OrderForm

    def get_context_main(self, context={}):
        device = self.request.COOKIES.get('sessionid', '')
        queryset = CartProduct.objects.filter(customer__uid_device=device)
        details = queryset \
                    .annotate(discount=F('product__price') * F('product__discount') * F('amount'), total=F('product__price') * F('amount')) \
                    .aggregate(Sum('discount', default=Value(0)), Sum('total', default=Value(0)))
        price_sending = 0 if self.request.POST.get('is_pickup') else PRICE_SENDING

        context['price_sending'] = price_sending
        context['discount'] = details['discount__sum']
        context['subtotal'] = details['total__sum']
        context['total'] = details['total__sum'] - details['discount__sum'] + price_sending
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_context_main(context)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            invoice_number = str(uuid.uuid4())

            device = self.request.COOKIES.get('sessionid', '')
            customer = Customer.objects.get(uid_device=device)
            queryset = CartProduct.objects.filter(customer__uid_device=device)
            details = queryset \
                        .annotate(discount=F('product__price') * F('product__discount') * F('amount'), total=F('product__price') * F('amount')) \
                        .aggregate(Sum('discount', default=Value(0)), Sum('total', default=Value(0)))

            is_pickup = True if request.POST.get('is_pickup', 'false') == 'on' else False
            price_sending = 0 if is_pickup else PRICE_SENDING
            date_expired = (datetime.now() + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S')

            total = int(details['total__sum'] - details['discount__sum'] + price_sending)

            order = Order(uid=invoice_number, 
                            customer=customer, 
                            address=request.POST['address'], 
                            is_pickup=is_pickup, 
                            type_payment=request.POST['type_payment'], 
                            price_sending=price_sending,
                            discount=details['discount__sum'],
                            total=total,
                            date_expired=date_expired,
                            date_schedule=request.POST['date_schedule'])
            order.save()

            for cart_product in queryset:
                order_product = OrderProduct(order=order, 
                                                product=cart_product.product, 
                                                color=cart_product.color, 
                                                note=cart_product.note, 
                                                amount=cart_product.amount, 
                                                price=cart_product.get_total)
                order_product.save()
            return redirect('/pago?ref_order='+order.uid)
        else:
            return render(request, "order.html", {"form": form, **self.get_context_main()})
        


class PaymentView(CreateView):
    model = Payment
    template_name = 'payment.html'
    form_class = PaymentForm

    def get_context_main(self, context={}):
        ref_order = self.request.GET.get('ref_order')

        device = self.request.COOKIES.get('sessionid', '')
        queryset = Order.objects.get(customer__uid_device=device, uid=ref_order)

        context['price_sending'] = queryset.price_sending
        context['discount'] = queryset.discount
        context['subtotal'] = queryset.total + queryset.discount - queryset.price_sending
        context['total'] = queryset.total
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_context_main(context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            ip = get_client_ip(request)
            invoice_number = str(uuid.uuid4())
            token = get_token_epayco()

            device = self.request.COOKIES.get('sessionid', '')
            ref_order = request.POST.get('ref_order')
            order = Order.objects.get(uid=ref_order)
            customer = customer = Customer.objects.get(uid_device=device)

            queryset = Order.objects.get(customer__uid_device=device, uid=ref_order)

            total = queryset.total

            payload = {
                "bank": request.POST['bank'],
                "value": str(total),
                "docType": request.POST['docType'],
                "docNumber": request.POST['num_document'],
                "name": request.POST['first_name'],
                "lastName": request.POST['last_name'],
                "email": request.POST['email'],
                "cellPhone": request.POST['cellphone'],
                "ip": ip,
                "urlResponse": settings.SUCCESS_PAYMENT,
                "description": "Compra ramos y detalles",
                "invoice": invoice_number,
                "currency": "COP",
                "address": request.POST['address']
            }
            payment_response = payment_pse(token, payload)
            if payment_response['success']:
                payment = Payment(transaction_id=payment_response['data']['transactionID'],
                                ref_payment=payment_response['data']['ref_payco'],
                                customer=customer, 
                                order=order, 
                                ref=ref_order, 
                                bank=request.POST['bank'], 
                                type_person=request.POST['typePerson'],
                                type_document=request.POST['docType'],
                                num_document=request.POST['num_document'],
                                first_name=request.POST['first_name'],
                                last_name=request.POST['last_name'],
                                email=request.POST['email'],
                                ip=ip,
                                cellphone=request.POST['cellphone'],
                                total=total)
                payment.save()
                CartProduct.objects.filter(customer__uid_device=device).delete()
                return redirect(payment_response['data']['urlbanco'])
            else:
                return redirect('/carrito')
        else:
            return render(request, "payment.html", {"form": form, **self.get_context_main()})