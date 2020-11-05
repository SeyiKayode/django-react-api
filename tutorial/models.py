from django.db import models

# Create your models here.

class Tutorial(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title 


