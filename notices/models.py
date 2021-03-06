from django.db import models
from accounts.models import Batch

# Create your models here.
class Notice(models.Model):
    notice = models.CharField(blank=False,max_length=200)
    batch = models.ForeignKey(Batch,on_delete=models.CASCADE,null=True,blank=True)
    published_at = models.DateField()
    created_at = models.DateField(auto_now=True)
    REQUIRED_FIELDS = ['notice','published_at']
