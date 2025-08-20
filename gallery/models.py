from django.db import models
from django.contrib.auth.models import User

# Profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'


# Photo model
class Photo(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='photos/')
    tags = models.CharField(max_length=200, blank=True)

    # New fields with null=True, blank=True for smooth migrations
    uploaded_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="uploaded_photos",
        null=True,
        blank=True
    )

    likes = models.ManyToManyField(User, related_name='photo_likes', blank=True)

    def __str__(self):
        return self.title
