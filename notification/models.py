from django.db import models
from accounts.models import User

# Create your models here.

class Notification(models.Model):
    notification = models.CharField(blank=False,max_length=200)
    to = models.ForeignKey(User, on_delete=models.CASCADE,null=False)
    read = models.BooleanField(default = False)
    created_at = models.DateField(auto_now=True)
    REQUIRED_FIELDS = ['notification','to']
