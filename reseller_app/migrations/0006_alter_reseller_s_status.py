# Generated by Django 4.1.2 on 2022-11-04 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reseller_app', '0005_reseller_s_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reseller',
            name='s_status',
            field=models.CharField(default='pending', max_length=12),
        ),
    ]
