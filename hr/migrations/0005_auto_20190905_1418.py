# Generated by Django 2.1.3 on 2019-09-05 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0004_house_hex_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='house',
            name='qr_code',
            field=models.ImageField(default='qr_codes/default-qr.jpg', upload_to='images/qr_codes'),
        ),
    ]