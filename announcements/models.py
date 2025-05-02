from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    image = CloudinaryField('image', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title