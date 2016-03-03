import arrow
from django.db import models
from django.conf import settings
from django.utils import timezone
# from .signals import subscription_created, subscription_was_cancelled
from paypal.standard.ipn.signals import subscription_signup, subscription_cancel


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


# def subscription_created(sender, **kwargs):
#
#     ipn_obj = sender
#     print ipn_obj
#     magazine_id = ipn_obj.custom.split('-')[0]
#     user_id = ipn_obj.custom.split('-')[1]
#     Purchase.objects.create(magazine_id=magazine_id,
#                             user_id=user_id,
#                             subscription_end=arrow.now().replace(weeks=+4).datetime)
#
#
# def subscription_was_cancelled(sender, **kwargs):
#
#     ipn_obj = sender
#     magazine_id = ipn_obj.custom.split('-')[0]
#     user_id = ipn_obj.custom.split('-')[1]
#     purchase = Purchase.object.get(user_id=user_id, magazine_id=magazine_id)
#     purchase.subscription_end = arrow.now()
#     purchase.save()
#
# subscription_signup.connect(subscription_created)
# subscription_cancel.connect(subscription_was_cancelled)