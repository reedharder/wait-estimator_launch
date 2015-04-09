from django.db import models
from django.contrib.auth.models import User


#model for each data input/processing session
class Session(models.Model):
    #link each session to a user
    user = models.ForeignKey(User)
    
class CapacitySave(models.Model):
    table = models.TextField()
    savetime=models.TextField()

    
class ProfileSave(models.Model):
    table = models.TextField()
    savetime=models.TextField()

