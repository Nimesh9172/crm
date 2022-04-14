from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_user = models.BooleanField('Is user',default=False)
    is_admin = models.BooleanField('Is admin',default=False)

# Create your models here.
class Customer(models.Model):
    created_by = models.CharField(max_length=100,null=True,blank=True)
    name = models.CharField(max_length=200,null=True,blank=True)
    phone = models.CharField(max_length=15,null=True,blank=True)
    productid = models.BigIntegerField()
    price = models.BigIntegerField()
    address =  models.CharField(max_length=255,null=True,blank=True)
    city = models.CharField(max_length=50,null=True,blank=True)
    disposition = models.CharField(max_length=50,null=True,blank=True)
    sub_disposition = models.CharField(max_length=50,null=True,blank=True)
    remarks = models.TextField(max_length=50)

    def __str__(self):
        return self.name

class ListUpload(models.Model):
    listid = models.CharField(max_length=200,unique=True)
    listname = models.CharField(max_length=200)
    created = models.DateField(auto_now_add = True,null=True)
    files = models.FileField(null=True)

class ExcelFormat(models.Model):
    dataformat = models.FileField(null=True)
    created = models.DateField(auto_now_add=True,null=True)