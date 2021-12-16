from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
# Create your models here.



class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="posts")
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.pk])


class Comment(models.Model):
    body = models.TextField(max_length=2000, help_text=None)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name="+", null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

