# models.py
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images/')
    caption = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    liked_by = models.ManyToManyField(User, related_name='liked_posts', blank=True)  # Track users who liked this post
    likes = models.PositiveIntegerField(default=0)  # To track the number of likes

    def __str__(self):
        return f"Post by {self.user.username} on {self.created_at}"

    def update_like_count(self):
        """Updates the like count based on the liked_by field."""
        self.likes = self.liked_by.count()
        self.save()
