from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views


urlpatterns = [
    path('bancos', views.get_banks, name='banks'),
    path('update_order', views.update_order, name='update-order'),
    path('orden', views.OrderView.as_view(), name='order'),
    path('pago', views.PaymentView.as_view(), name='payment'),
    path('update_cart/<int:pk>/<int:type>', views.update_cart, name='update-cart'),
    path('carrito', views.CartView.as_view(), name='carrito'),
    path('producto/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('producto/<str:category>', views.CategoryListView.as_view(), name='product-category'),
    path('', views.MainListView.as_view(), name='main')
]