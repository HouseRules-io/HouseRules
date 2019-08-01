# Generated by Django 2.1.3 on 2019-08-01 22:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('house_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rule_name', models.CharField(max_length=50)),
                ('rule_text', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Rulebook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rulebook_name', models.CharField(max_length=50)),
                ('parent_house', models.ForeignKey(default='0000000', on_delete=django.db.models.deletion.CASCADE, to='hr.House')),
            ],
        ),
        migrations.AddField(
            model_name='rule',
            name='parent_rulebook',
            field=models.ForeignKey(default='0000000', on_delete=django.db.models.deletion.CASCADE, to='hr.Rulebook'),
        ),
    ]
