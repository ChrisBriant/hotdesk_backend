from django.db import models
from accounts.models import Account
from desks.models import Desk

#NOT NECESSARY
class Slot(models.Model):
    date = models.DateTimeField(null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['date'], name='unique_slot')
        ]


class Booking(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    desk = models.ForeignKey(Desk,on_delete=models.CASCADE)
    date = models.DateTimeField(null=False)
    date_booked = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['date','desk','user'], name='unique_booking')
        ]
