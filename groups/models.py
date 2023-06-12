from django.db import models


class Group(models.Model):
    id: models.IntegerField(unique=True, null=False)
    scientific_name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
