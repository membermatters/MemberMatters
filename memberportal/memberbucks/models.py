from django.db import models
from django.conf import settings
from django.db.models import Sum


class MemberBucks(models.Model):
    class Meta:
        verbose_name = "Memberbucks"
        verbose_name_plural = "Memberbucks"

    TRANSACTION_TYPES = (
        ("stripe", "Stripe Top-up"),  # used to track credits via Stripe
        ("bank", "Bank Transfer"),  # could be for a debit or credit
        ("cash", "Cash"),  # could be for a debit or credit
        (
            "card",
            "Membership Card",
        ),  # used to track debits from vending machines / debit endpoints
        (
            "interlock",
            "Interlock Cost",
        ),  # used to track automatic debits from interlock sessions
        ("other", "Other"),
    )

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.FloatField("Amount")
    transaction_type = models.CharField(
        "Transaction Type", max_length=10, choices=TRANSACTION_TYPES
    )
    description = models.CharField("Description of Transaction", max_length=100)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    logging_info = models.TextField("Detailed logging info from stripe.", blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} {'debited' if self.amount > 0 else 'credited'} ${abs(self.amount)} for {self.description} on {self.date.date()}"

    def save(self, *args, **kwargs):
        super(MemberBucks, self).save(*args, **kwargs)
        balance = MemberBucks.objects.filter(user=self.user).aggregate(Sum("amount"))[
            "amount__sum"
        ]
        self.user.profile.memberbucks_balance = round(balance, 2)
        self.user.profile.save()

    def get_transaction_display(self):
        return {
            "amount": self.amount,
            "type": self.get_transaction_type_display(),
            "description": self.description,
            "date": self.date,
        }
