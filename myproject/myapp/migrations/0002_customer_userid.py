# Generated by Django 4.0.3 on 2022-04-11 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='userid',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
