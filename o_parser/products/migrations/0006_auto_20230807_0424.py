# Generated by Django 3.2.20 on 2023-08-06 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_product_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='id_request',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='productpost',
            name='created',
            field=models.DateTimeField(db_index=True, default='2023-01-01 00:00'),
        ),
        migrations.AddField(
            model_name='productpost',
            name='id_request',
            field=models.TextField(default=''),
        ),
    ]