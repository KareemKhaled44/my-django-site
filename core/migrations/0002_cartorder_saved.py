# Generated by Django 5.1.3 on 2025-06-10 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartorder',
            name='saved',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
