# Generated by Django 4.1.2 on 2022-10-27 05:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reseller_app', '0003_alter_product_seller'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='seller',
            new_name='seller_id',
        ),
    ]