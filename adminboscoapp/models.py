from django.db import models
from django.contrib.auth.models import User

class Theater(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    theater_name = models.CharField(max_length=200)
    theater_image = models.ImageField(upload_to='images/')
    owner_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    location = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    manager_name = models.CharField(max_length=200)
    approved = models.BooleanField(default=True)
    
    
class Movie(models.Model):
    theater_name = models.ForeignKey(Theater, on_delete=models.CASCADE, blank=True, null=True)
    movie_name = models.CharField(max_length=50)
    movie_trailer = models.FileField(upload_to='movies/trailers/', null=True, blank=True)
    movie_rdate = models.DateField(null=True, blank=True)  # Using DateField for release date
    movie_des = models.TextField()
    movie_rating = models.DecimalField(max_digits=3, decimal_places=1)
    movie_poster = models.ImageField(upload_to='movies/poster', default="movies/poster/not.jpg")
    movie_genre = models.CharField(max_length=50, default="Action | Comedy | Romance")
    movie_duration = models.CharField(max_length=10, default="2hr 45min")



class Shows(models.Model):
    theater_name = models.ForeignKey(Theater, on_delete=models.CASCADE, blank=True, null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_show')
    time = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(null=True, blank=True)
    price = models.IntegerField()