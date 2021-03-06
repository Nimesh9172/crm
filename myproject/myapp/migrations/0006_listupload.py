# Generated by Django 4.0.3 on 2022-04-12 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_alter_customer_created_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listid', models.CharField(max_length=200, unique=True)),
                ('listname', models.CharField(max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('files', models.FileField(null=True, upload_to='')),
            ],
        ),
    ]
