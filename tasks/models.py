from django.db import models
from django.contrib.auth.models import User


class Tasks(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title + " - By: " + self.author.username
