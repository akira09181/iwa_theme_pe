from django.db import models
from django.db.models.fields import CharField

# Create your models here.
class Users(models.Model):
    id = models.CharField(max_length=30,verbose_name='Gmailアドレス',primary_key=True)

class Mails(models.Model):
    name = models.CharField(default = "",max_length=100)
    date = models.CharField(default = "",max_length=100)
    domain = models.CharField(default = "",max_length=100)
    title = models.CharField(primary_key=True,default = "",max_length=200)