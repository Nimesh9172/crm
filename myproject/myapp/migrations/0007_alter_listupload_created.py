# Generated by Django 4.0.3 on 2022-04-12 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_listupload'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listupload',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
