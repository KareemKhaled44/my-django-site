# Generated by Django 5.1.3 on 2025-06-12 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_cartorderitem_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartorderitem',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='order'),
        ),
    ]
