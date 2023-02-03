# Generated by Django 3.1.7 on 2023-02-02 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_product_users_wishlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discount_price',
            field=models.DecimalField(decimal_places=2, error_messages={'name': {'max_length': 'The price must be between 0 and 99999.99.'}}, help_text='Maximum 99999.99', max_digits=5, verbose_name='Discount price'),
        ),
        migrations.AlterField(
            model_name='product',
            name='regular_price',
            field=models.DecimalField(decimal_places=2, error_messages={'name': {'max_length': 'The price must be between 0 and 99999.99.'}}, help_text='Maximum 99999.99', max_digits=7, verbose_name='Regular price'),
        ),
    ]
