from django.db import models

# Create your models here.
class UserProfile(models.Model):
    username = models.CharField(max_length=30,blank=True, null=True)  # Add this line
    firstname = models.CharField(max_length=30,blank=True, null=True)
    lastname = models.CharField(max_length=30,blank=True, null=True)
    email = models.EmailField()
    mobile = models.CharField(max_length=15, blank=True, null=True)