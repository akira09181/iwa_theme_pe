from django.db import models
from django.db.models.fields import CharField

# Create your models here.
class Users(models.Model):
    id = models.CharField(max_length=30,verbose_name='Gmailアドレス',primary_key=True)

class Mails(models.Model):
    no = models.IntegerField(default=0,primary_key=True)
    date = models.CharField(default = "",max_length=100,null=True)
    domain = models.CharField(default = "",max_length=100)
    title = models.CharField(default = "",max_length=200)
    now = models.CharField(default="",max_length=100)