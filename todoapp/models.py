from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.db import models

class Task(models.Model):
    description = models.CharField(max_length=4096)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.description