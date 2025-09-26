from django.db import models
from django.contrib.auth.models import AbstractUser


#every user have his own Team 
class Team(models.Model):
    
    team_name = models.CharField(max_length=250)
    manager = models.CharField(max_length=250, blank=True,)
    
    def __str__(self):
        return self.team_name


class CustomUser(AbstractUser):

    team_id = models.ForeignKey(Team, on_delete=models.CASCADE, null= True, blank=True)
    username= models.CharField(max_length=250, unique=True, null=True)
    #username= None
    #email = models.EmailField("email address", unique=True)
    
    #USERNAME_FIELD ="email"
    #REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.username
    
    
    