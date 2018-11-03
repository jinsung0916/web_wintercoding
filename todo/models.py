# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Todo(models.Model):
    title = models.CharField(max_length=100, default='')
    content = models.TextField(max_length=500, default='')
    priority = models.IntegerField(
        default=3,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ]
    )
    dueDate = models.DateTimeField(null=True)
    isFulfilled = models.BooleanField(default=False)

    class Meta:
        ordering = ('dueDate', 'priority')
