from django.db import models
from django.db.models.fields import CharField

# Create your models here.
class Users(models.Model):
    id = models.CharField(max_length=30,primary_key=True,verbose_name='Gmailアドレス')
    pas = models.CharField(max_length=20,verbose_name='パスワード')
