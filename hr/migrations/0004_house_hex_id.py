# Generated by Django 2.1.3 on 2019-09-05 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0003_auto_20190903_1337'),
    ]

    operations = [
        migrations.AddField(
            model_name='house',
            name='hex_id',
            field=models.CharField(default=-1, max_length=20),
            preserve_default=False,
        ),
    ]
