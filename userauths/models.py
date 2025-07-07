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
    STATUS_CHOICES = [
        ('new', 'New'),                  # Default when user submits the form
        ('in_progress', 'In Progress'), # Being handled
        ('on_hold', 'On Hold'),         # Waiting for user or external input
        ('resolved', 'Resolved'),       # Successfully handled
        ('spam', 'Spam'),               # Detected as spam
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)  # Optional field for phone number
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
    )

    def __str__(self):
        return self.full_name