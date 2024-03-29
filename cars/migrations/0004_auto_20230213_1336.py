# Generated by Django 3.2.17 on 2023-02-13 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0003_auto_20230210_0907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auto',
            name='frame',
            field=models.CharField(choices=[('bus', 'Bus'), ('microbus', 'Microbus'), ('minivan', 'Minivan'), ('sedan', 'Sedan'), ('pickup', 'Pickup'), ('universal', 'Universal'), ('hatchback', 'Hatchback'), ('other', 'Other')], default='sedan', max_length=50),
        ),
        migrations.AlterField(
            model_name='auto',
            name='fuel',
            field=models.CharField(choices=[('gas', 'Gas'), ('diesel', 'Diesel'), ('electro', 'Electro'), ('petrol', 'Petrol'), ('hybrid', 'Hybrid')], default='petrol', max_length=25),
        ),
        migrations.AlterField(
            model_name='auto',
            name='origin',
            field=models.CharField(choices=[('Asia', 'Asia'), ('Europe', 'Europe'), ('America', 'America'), ('other', 'Other')], default='Europe', max_length=50),
        ),
        migrations.AlterField(
            model_name='auto',
            name='transmission',
            field=models.CharField(choices=[('mech', 'Mech'), ('auto', 'Auto')], default='auto', max_length=25),
        ),
    ]
