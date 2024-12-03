from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit

# Create your models here.
from django.db import models

class Task(models.Model):
    description = models.CharField(max_length=4096)
    completed = models.BooleanField(default=False)
    icon = models.ImageField(upload_to="task_icons", blank=True)
    thumbnail = ImageSpecField(
        source='icon',
        processors=[ResizeToFit(100,100)],
        format='JPEG',
        options={'quality': 70},
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.description