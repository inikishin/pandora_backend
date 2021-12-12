"""
News Django App
"""

import uuid
from django.db import models


class Source(models.Model):
    """
    News source model
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fullname = models.TextField()
    url = models.TextField()
    parameters = models.TextField()

    def __repr__(self):
        return f'{self.fullname} (id: {self.id})'

    def __str__(self):
        return f'{self.fullname}'


class Tag(models.Model):
    """
    News tag model
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tag_name = models.CharField(max_length=100)

    def __repr__(self):
        return f'{self.tag_name} (id: {self.id})'

    def __str__(self):
        return f'{self.tag_name}'


class News(models.Model):
    """
    News model
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    datetime = models.DateTimeField()
    text = models.TextField()
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)
    def __repr__(self):
        return f'{self.text[:50]} (source: {self.source})'

    def __str__(self):
        return f'{self.text[:50]}'
