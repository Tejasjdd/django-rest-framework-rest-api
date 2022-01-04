# Generated by Django 4.0 on 2021-12-28 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_order_order_status_alter_order_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('PENDING', 'pending'), ('IN-TRANSIT', 'in-transit'), ('DELIVERED', 'delivered')], default='PENDING', max_length=20),
        ),
    ]
