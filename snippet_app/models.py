from django.db import models
from django.contrib.auth.models import User

class TagTable(models.Model):
    title = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.title

class ContentTable(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ForeignKey(TagTable, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title
