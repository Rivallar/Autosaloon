# Generated by Django 3.2.18 on 2023-02-20 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0006_delete_autosaloon_delete_salooncars'),
    ]

    operations = [
        migrations.AddField(
            model_name='dealer',
            name='buyer_discounts',
            field=models.JSONField(default=dict),
        ),
    ]
