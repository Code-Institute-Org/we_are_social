from django.db import models
from django.conf import settings
from django.utils import timezone


class Magazine(models.Model):

    name = models.CharField(max_length=254, default='')
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __unicode__(self):
        return self.name


class Purchase(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='purchases')
    magazine = models.ForeignKey(Magazine)
    subscription_end = models.DateTimeField(default=timezone.now())


from signals import subscription_created, subscription_was_cancelled
from paypal.standard.ipn.signals import valid_ipn_received

valid_ipn_received.connect(subscription_created)
valid_ipn_received.connect(subscription_was_cancelled)
