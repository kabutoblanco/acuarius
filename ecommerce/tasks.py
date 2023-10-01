from django.core.mail import send_mail

from .models import Payment, Order, STATUS_PAYMENT_DICT, STATUS_ORDER_DICT
from .services import get_status_payment, get_token_epayco

from celery import shared_task


@shared_task(name='check_payments')
def check_payments():
    try:
        token = get_token_epayco()
        payments_standby = Payment.objects.filter(status=STATUS_PAYMENT_DICT['PENDING'])
        for payment in payments_standby:
            status_payment = get_status_payment(token, {'filter': {'referencePayco': payment.ref_payment}})
            if status_payment['success']:
                status = status_payment['data']['status']
                order = Order.objects.get(id=payment.order.id)
                if status == 'Aceptada':
                    payment.status = STATUS_PAYMENT_DICT['APPROVADED']
                    order.status = STATUS_ORDER_DICT['APPROVADED']

                    subject = 'Pedido aprovado'
                    message = f"El pedido No.{order.uid} fue pagado exitosamente por un valor de {payment.total}, el día y hora de entrega es {order.date_schedule}."
                    from_email = 'notificaciones@acuariusfloristeriacali.com'
                    recipient_list = ['mdquilindo@unicauca.edu.co']

                    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                    print('Sending email to Floristeria confirm payment')
                elif status == 'Cancelada':
                    payment.status = STATUS_PAYMENT_DICT['CANCELED']
                    order.status = STATUS_ORDER_DICT['CANCELED']
                    print('Change status order to canceled')
                else:
                    print('Again pending')
                payment.save()
                order.save()
    except Exception as e:
        print(f"Error: {str(e)}")