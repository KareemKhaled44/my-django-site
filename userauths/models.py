from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
 

class User(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    """
    email = models.EmailField(unique=True)
    username= models.CharField(max_length=100, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
      return self.username
    
class Contact(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return self.full_name