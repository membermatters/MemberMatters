from django.db import models


# This is a Stripe Product
class MemberTier(models.Model):
    """[A membership tier that a member can be billed for.]"""

    name = models.CharField("Name", max_length=30, unique=True)
    description = models.CharField("Description", max_length=50, unique=True)
    stripe_id = models.CharField("Stripe Id", max_length=100, unique=True)
    visible = models.BooleanField("Is this plan visible to members?", default=True)
    featured = models.BooleanField("Is this plan featured?", default=False)

    def __str__(self):
        return self.name


# This is a Stripe Price
class PaymentPlan(models.Model):
    """[A payment plan that specifies how a member is billed for a member tier.]"""

    BILLING_PERIODS = [("Months", "month"), ("Weeks", "week"), ("Days", "days")]

    name = models.CharField("Name", max_length=30)
    stripe_id = models.CharField("Stripe Id", max_length=100, unique=True)
    member_tier = models.ForeignKey(
        MemberTier, on_delete=models.CASCADE, related_name="plans"
    )
    visible = models.BooleanField("Is this plan visible to members?", default=True)
    currency = models.CharField(
        "Three letter ISO currency code.", max_length=3, default="aud"
    )
    cost = models.IntegerField("The cost in cents for this payment plan.")
    interval_count = models.IntegerField(
        "How frequently the price is charged at (per billing interval)."
    )
    interval = models.CharField(choices=BILLING_PERIODS, max_length=10)

    def __str__(self):
        return self.name
