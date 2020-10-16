from django.db import models
from classlinks.models import ClassLink
from accounts.models import Batch,User

# Create your models here.
class Vedio(models.Model):
    classlink = models.ForeignKey(ClassLink,on_delete=models.CASCADE,null=False)

    title = models.CharField(blank=False,max_length=255)
    url = models.URLField(max_length=200)
    created_at = models.DateField(auto_now=True)

    REQUIRED_FIELDS = ['classlink','title','url']
