from django.db import models

# Create your models here.


class User_info(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=60)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
