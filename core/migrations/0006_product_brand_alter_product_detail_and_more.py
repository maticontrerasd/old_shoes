# Generated by Django 4.2.1 on 2024-05-30 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.CharField(default=1223, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='detail',
            field=models.TextField(max_length=500, verbose_name='Informacion del producto'),
        ),
        migrations.AlterField(
            model_name='product',
            name='excerpt',
            field=models.TextField(max_length=300, verbose_name='Extracto'),
        ),
    ]
