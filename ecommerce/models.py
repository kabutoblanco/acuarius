from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _


TYPE_PERSON = ((1, _("NATURAL")), (2, _("JURIDICA")))
TYPE_DOCUMENT = (("CC", _("CC")), ("NIT", _("NIT")), ("PPN", _("PASAPORTE")))
TYPE_PRODUCT = ((1, _("PRINCIPAL")), (2, _("DETAIL")))
TYPE_PAYMENT = ((1, _("PSE")), (2, _("TRANSFERENCIA")))
STATUS_ORDER = ((1, _("RECEIVED")), (2, _("SENDED")), (3, _("DELIVERED")))
STATUS_PAYMENT = ((1, _("PENDING")), (2, _("APPROVADED")), (3, _("CANCELED")))

# Create your models here.
class Customer(models.Model):
    uid_device = models.CharField(null=True, blank=True, unique=True, max_length=120, verbose_name='UID')
    email = models.EmailField(null=True, blank=True, unique=True, verbose_name='Correo')

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural= 'Clientes'

    def __str__(self) -> str:
        return '[{}] - {} {}'.format(self.id, self.uid_device, self.email)


class Color(models.Model):
    name = models.CharField(max_length=65, verbose_name='Nombre')
    ref = models.CharField(max_length=45, verbose_name='Código HEX')

    class Meta:
        verbose_name = 'Color'
        verbose_name_plural= 'Colores'

    def __str__(self) -> str:
        return '[{}] - {}'.format(self.id, self.name)


class Category(models.Model):
    name = models.CharField(max_length=65, verbose_name='Nombre')
    path = models.CharField(max_length=65, verbose_name='Ruta')

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural= 'Categorias'

    def __str__(self) -> str:
        return '[{}] - {}'.format(self.id, self.name)


class Product(models.Model):
    type_product = models.IntegerField(choices=TYPE_PRODUCT, default=1, verbose_name='Tipo')
    name = models.CharField(max_length=200, verbose_name='Nombre')
    price = models.IntegerField(verbose_name='Precio')
    discount = models.FloatField(verbose_name='Descuento')
    colors = models.ManyToManyField('ecommerce.Color', verbose_name='Colores')
    categories = models.ManyToManyField('ecommerce.Category', blank=True, verbose_name='Categorias')
    image_1 = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name='Imagen 1')
    image_2 = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name='Imagen 2')
    image_3 = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name='Imagen 3')
    description = models.TextField(verbose_name='Descripción')

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural= 'Productos'

    def __str__(self) -> str:
        return '[{}] - {}'.format(self.id, self.name)

    @property
    def get_discount_percentange(self):
        discount = self.discount * 100
        return discount

    def format_price(self):
        num_str = str(self.price)
        token = []
        count = 0

        for digit in num_str[::-1]:
            if count == 3:
                token.append(',')
                count = 0
            token.append(digit)
            count += 1

        return format_html('<span>{}</span/>', '$' + ''.join(token[::-1]))

    format_price.admin_order_field = 'price' 


class CartProduct(models.Model):
    customer = models.ForeignKey('ecommerce.Customer', on_delete=models.CASCADE, verbose_name='Cliente')
    product = models.ForeignKey('ecommerce.Product', on_delete=models.CASCADE, verbose_name='Producto')
    color = models.CharField(max_length=50, verbose_name='Color')
    note = models.TextField(verbose_name='Nota')
    amount = models.IntegerField(verbose_name='Cantidad')

    class Meta:
        verbose_name = 'Carrito'
        verbose_name_plural= 'Carritos'

    def __str__(self) -> str:
        return '[{}] - {} {}'.format(self.id, self.customer, self.product)

    @property
    def get_discount(self):
        total = (self.product.price * self.product.discount) * self.amount
        return total

    @property
    def get_total(self):
        total = self.product.price * self.amount - (self.product.price * self.product.discount) * self.amount
        return total


class Order(models.Model):
    uid = models.UUIDField(max_length=255, verbose_name='Referencia')
    customer = models.ForeignKey('ecommerce.Customer', on_delete=models.CASCADE, verbose_name='Cliente')
    status = models.IntegerField(choices=STATUS_ORDER, default=1, verbose_name='Estado')
    address = models.CharField(max_length=255, verbose_name='Dirección de entrega')
    is_pickup = models.BooleanField(default=False, verbose_name='¿Recoge en la tienda?')
    type_payment = models.IntegerField(choices=TYPE_PAYMENT, default=1, verbose_name='Tipo de pago')
    price_sending = models.IntegerField(verbose_name='Costo de envio')
    discount = models.IntegerField(verbose_name='Descuento')
    total = models.IntegerField(verbose_name='Total')
    date_expired = models.DateTimeField(verbose_name='Fecha expiración')
    date_schedule = models.DateTimeField(verbose_name='Fecha programada')

    class Meta:
        verbose_name = 'Orden'
        verbose_name_plural= 'Ordenes'

    def __str__(self) -> str:
        return '[{}]'.format(self.uid)


class OrderProduct(models.Model):
    order = models.ForeignKey(to='ecommerce.Order', on_delete=models.CASCADE, verbose_name='Orden')
    product = models.ForeignKey('ecommerce.Product', on_delete=models.CASCADE, verbose_name='Producto')
    color = models.CharField(max_length=50, verbose_name='Color')
    note = models.TextField(verbose_name='Nota')
    amount = models.IntegerField(verbose_name='Cantidad')
    price = models.IntegerField(verbose_name='Precio')

    class Meta:
        verbose_name = 'Orden'
        verbose_name_plural= 'Ordenes'

    def __str__(self) -> str:
        return '{} - {} {}'.format(self.id, self.order, self.product)


class Payment(models.Model):
    customer = models.ForeignKey(to='ecommerce.Customer', on_delete=models.CASCADE, verbose_name='Cliente')
    status = models.IntegerField(choices=STATUS_PAYMENT, default=1, verbose_name='Estado')
    order = models.ForeignKey(to='ecommerce.Order', on_delete=models.CASCADE, verbose_name='Orden')
    ref = models.CharField(max_length=255, verbose_name='Referencia')
    bank = models.CharField(max_length=255, verbose_name='Banco')
    type_person = models.IntegerField(choices=TYPE_PERSON, default=1, verbose_name='Tipo persona')
    type_document = models.CharField(choices=TYPE_DOCUMENT, max_length=255, default="CC", verbose_name='Tipo de documento')
    num_document = models.CharField(max_length=255, verbose_name='No. documento')
    first_name = models.CharField(max_length=255, verbose_name='Nombres')
    last_name = models.CharField(max_length=255, verbose_name='Apellidos')
    email = models.EmailField(max_length=255, verbose_name='Correo')
    ip = models.CharField(max_length=255, verbose_name='Ip')
    cellphone = models.CharField(max_length=255, verbose_name='Celular')
    total = models.IntegerField(verbose_name='Total')

    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural= 'Pagos'

    def __str__(self) -> str:
        return '[{}] - {} {}'.format(self.id, self.order, self.status)