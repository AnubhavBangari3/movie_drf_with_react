from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Movie(models.Model):
    gen=(('drama','drama'),('action','action'),('adventure','adventure'),('fantasy','fantasy'),('thriller','thriller'),('horror','horror'),
         ('comedy','comedy'))
    title=models.CharField(max_length=256)
    director=models.CharField(max_length=256)
    stars=models.CharField(max_length=256)
    genre=models.CharField(choices=gen,max_length=20)
    like=models.ManyToManyField(User,blank=True,related_name="like")
    unlike=models.ManyToManyField(User,blank=True,related_name="unlike")
    
    def __str__(self):
        return str(self.title)
    
class Like(models.Model):
    userL=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_liked")
    movieL=models.ForeignKey(Movie,on_delete=models.CASCADE,related_name="movie_liked")
    
    def __str__(self):
        return f"{self.userL} liked {self.movieL}"
    
class DisLike(models.Model):
    userDL=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_disliked")
    movieDL=models.ForeignKey(Movie,on_delete=models.CASCADE,related_name="movie_disliked")
    
    def __str__(self):
        return f"{self.userDL} disliked {self.movieDL}"