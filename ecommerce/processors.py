from .models import Category, CartProduct


def navbar(request):
    if not request.session.session_key:
        request.session['guest'] = True
    device = request.COOKIES.get('sessionid', '')
    categories = Category.objects.all()
    cart_count = CartProduct.objects.filter(customer__uid_device=device).count()

    return { 'categories': categories, 'cart_count': cart_count }