from django.db import models
from django.utils import timezone


class ContactModel(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=250)
    topic = models.CharField(max_length=200)
    message = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.email

    class Meta:
        ordering = ['-timestamp']