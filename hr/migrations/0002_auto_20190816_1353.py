# Generated by Django 2.1.3 on 2019-08-16 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rule',
            name='icon_link',
            field=models.CharField(default='fas fa-home', max_length=25),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='rulebook',
            name='icon_link',
            field=models.CharField(max_length=25),
        ),
    ]