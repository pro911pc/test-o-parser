# Generated by Django 3.2.20 on 2023-08-02 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('products_count', models.IntegerField(default=10)),
            ],
        ),
    ]
