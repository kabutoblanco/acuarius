# Generated by Django 4.2.4 on 2023-08-08 03:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=65, verbose_name='Nombre')),
                ('path', models.CharField(max_length=65, verbose_name='Ruta')),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=65, verbose_name='Nombre')),
                ('ref', models.CharField(max_length=45, verbose_name='Código HEX')),
            ],
            options={
                'verbose_name': 'Color',
                'verbose_name_plural': 'Colores',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid_device', models.CharField(blank=True, max_length=120, null=True, unique=True, verbose_name='UID')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='Correo')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(verbose_name='Referencia')),
                ('status', models.IntegerField(choices=[(1, 'RECEIVED'), (2, 'SENDED'), (3, 'DELIVERED')], default=1, verbose_name='Estado')),
                ('address', models.CharField(max_length=255, verbose_name='Dirección de entrega')),
                ('is_pickup', models.BooleanField(default=False, verbose_name='¿Recoge en la tienda?')),
                ('type_payment', models.IntegerField(choices=[(1, 'PSE'), (2, 'TRANSFERENCIA')], default=1, verbose_name='Tipo de pago')),
                ('price_sending', models.IntegerField(verbose_name='Costo de envio')),
                ('discount', models.IntegerField(verbose_name='Descuento')),
                ('total', models.IntegerField(verbose_name='Total')),
                ('date_expired', models.DateTimeField(verbose_name='Fecha expiración')),
                ('date_schedule', models.DateTimeField(verbose_name='Fecha programada')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.customer', verbose_name='Cliente')),
            ],
            options={
                'verbose_name': 'Orden',
                'verbose_name_plural': 'Ordenes',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_product', models.IntegerField(choices=[(1, 'PRINCIPAL'), (2, 'DETAIL')], default=1, verbose_name='Tipo')),
                ('name', models.CharField(max_length=200, verbose_name='Nombre')),
                ('price', models.IntegerField(verbose_name='Precio')),
                ('discount', models.FloatField(verbose_name='Descuento')),
                ('image_1', models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Imagen 1')),
                ('image_2', models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Imagen 2')),
                ('image_3', models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Imagen 3')),
                ('description', models.TextField(verbose_name='Descripción')),
                ('categories', models.ManyToManyField(blank=True, to='ecommerce.category', verbose_name='Categorias')),
                ('colors', models.ManyToManyField(to='ecommerce.color', verbose_name='Colores')),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(1, 'PENDING'), (2, 'APPROVADED'), (3, 'CANCELED')], default=1, verbose_name='Estado')),
                ('ref', models.CharField(max_length=255, verbose_name='Referencia')),
                ('bank', models.CharField(max_length=255, verbose_name='Banco')),
                ('type_person', models.IntegerField(choices=[(1, 'NATURAL'), (2, 'JURIDICA')], default=1, verbose_name='Tipo persona')),
                ('type_document', models.CharField(choices=[('CC', 'CC'), ('NIT', 'NIT'), ('PPN', 'PASAPORTE')], default='CC', max_length=255, verbose_name='Tipo de documento')),
                ('num_document', models.CharField(max_length=255, verbose_name='No. documento')),
                ('first_name', models.CharField(max_length=255, verbose_name='Nombres')),
                ('last_name', models.CharField(max_length=255, verbose_name='Apellidos')),
                ('email', models.EmailField(max_length=255, verbose_name='Correo')),
                ('ip', models.CharField(max_length=255, verbose_name='Ip')),
                ('cellphone', models.CharField(max_length=255, verbose_name='Celular')),
                ('total', models.IntegerField(verbose_name='Total')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.customer', verbose_name='Cliente')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.order', verbose_name='Orden')),
            ],
            options={
                'verbose_name': 'Pago',
                'verbose_name_plural': 'Pagos',
            },
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=50, verbose_name='Color')),
                ('note', models.TextField(verbose_name='Nota')),
                ('amount', models.IntegerField(verbose_name='Cantidad')),
                ('price', models.IntegerField(verbose_name='Precio')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.order', verbose_name='Orden')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.product', verbose_name='Producto')),
            ],
            options={
                'verbose_name': 'Orden',
                'verbose_name_plural': 'Ordenes',
            },
        ),
        migrations.CreateModel(
            name='CartProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=50, verbose_name='Color')),
                ('note', models.TextField(verbose_name='Nota')),
                ('amount', models.IntegerField(verbose_name='Cantidad')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.customer', verbose_name='Cliente')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.product', verbose_name='Producto')),
            ],
            options={
                'verbose_name': 'Carrito',
                'verbose_name_plural': 'Carritos',
            },
        ),
    ]
