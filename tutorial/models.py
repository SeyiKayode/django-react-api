from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Tutorial(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title 


class CustomUser(AbstractUser):
    fav_color = models.CharField(max_length=120)
