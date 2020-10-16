from django.db import models
from accounts.models import Batch
from accounts.models import User,Batch
#
# # Create your models here.
#
class Subject(models.Model):
    name = models.CharField(blank=False,max_length=200)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE,null=False)
    REQUIRED_FIELDS = ['name','batch']
#
class Classtime(models.Model):
    starttime = models.TimeField()
    endtime = models.TimeField()
    REQUIRED_FIELDS = ['time']

    def __str__(self):
        return str(self.starttime) + " - " + str(self.endtime)
#
class ClassLink(models.Model):
    """docstring for ."""
    teacher = models.ForeignKey(User, on_delete=models.CASCADE,null=False)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE,null=False)
    classdate = models.DateField()
    classtime = models.ForeignKey(Classtime,on_delete=models.CASCADE,null=False)
    url = models.URLField(max_length=200,null=False)
    created_at = models.DateField(auto_now=True)
    REQUIRED_FIELDS = ['batch','teacher','url','subject','classdate','classtime']
