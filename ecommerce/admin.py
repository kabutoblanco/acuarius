from django.contrib import admin
from django.utils.html import format_html

from .models import *


class BannerAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_preview')
    readonly_fields = ('date_record', 'date_update')
    search_fields = ('name',)
    ordering = ('name',)

    def image_preview(self, obj):
        if obj.img_small:
            return format_html('<img src="{}" width="40" height="40" />', obj.img_small.url)
        return None

    image_preview.short_description = 'Imagen pequeña'


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('uid_device', 'email')
    readonly_fields = ('date_record', 'date_update')
    search_fields = ('uid_device', 'email')
    ordering = ('uid_device', 'email')


class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'ref')
    readonly_fields = ('date_record', 'date_update')
    search_fields = ('name', 'ref')
    ordering = ('name', 'ref')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'path')
    readonly_fields = ('date_record', 'date_update')
    search_fields = ('name', 'path')
    ordering = ('name', 'path')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'format_price_view', 'image_preview')
    readonly_fields = ('date_record', 'date_update')
    search_fields = ('name',)
    ordering = ('name', 'price')

    def format_price_view(self, obj):
        return '${:,.0f}'.format(obj.price)

    def image_preview(self, obj):
        if obj.image_1:
            return format_html('<img src="{}" width="40" height="40" />', obj.image_1.url)
        return None

    format_price_view.short_description = 'Precio'
    image_preview.short_description = 'Imagen'


class CartProductAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'amount', 'format_price_view')
    readonly_fields = ('date_record', 'date_update')
    search_fields = ('product',)

    def format_price_view(self, obj):
        return '${:,.0f}'.format(obj.get_total)

    format_price_view.short_description = 'Total'


class OrderAdmin(admin.ModelAdmin):
    list_display = ('uid', 'status', 'format_price_view', 'date_schedule')
    readonly_fields = ('type_payment', 'date_record', 'date_update')
    search_fields = ('uid',)

    def format_price_view(self, obj):
        return '${:,.0f}'.format(obj.total)

    format_price_view.short_description = 'Total'


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('ref', 'status', 'format_price_view')
    readonly_fields = ('date_record', 'date_update')
    search_fields = ('ref',)

    def format_price_view(self, obj):
        return '${:,.0f}'.format(obj.order.total)

    format_price_view.short_description = 'Total'


# Register your models here.
admin.site.register(Banner, BannerAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(CartProduct, CartProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment, PaymentAdmin)