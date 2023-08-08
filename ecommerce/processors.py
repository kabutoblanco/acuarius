from .models import Category, CartProduct


def navbar(request):
    device = request.COOKIES.get('sessionid', '')
    categories = Category.objects.all()
    cart_count = CartProduct.objects.filter(customer__uid_device=device).count()

    return { 'categories': categories, 'cart_count': cart_count }