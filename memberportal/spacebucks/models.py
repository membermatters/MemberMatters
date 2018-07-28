from django.db import models
from django.conf import settings
from django.db.models import Sum


class SpaceBucks(models.Model):
    TRANSACTION_TYPES = (
        ('stripe', 'Stripe Payment'),
        ('bank', 'Bank Transfer'),
        ('card', 'Membership Card')
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.FloatField("Amount")
    transaction_type = models.CharField(
        "Transaction Type", max_length=10, choices=TRANSACTION_TYPES)
    description = models.CharField(
        "Description of Transaction", max_length=100)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    logging_info = models.TextField(
        "Detailed logging info from stripe.", blank=True)

    def save(self, *args, **kwargs):
        super(SpaceBucks, self).save(*args, **kwargs)
        balance = SpaceBucks.objects.filter(
            user=self.user).aggregate(Sum('amount'))['amount__sum']
        self.user.profile.spacebucks_balance = balance
        self.user.profile.save()
