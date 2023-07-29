from django.db import models


# This is a Stripe Product
class MemberTier(models.Model):
    """A membership tier that a member can be billed for."""

    id = models.AutoField(primary_key=True)
    name = models.CharField("Name", max_length=150, unique=True)
    description = models.CharField("Description", max_length=250, unique=True)
    stripe_id = models.CharField("Stripe Id", max_length=100, unique=True)
    visible = models.BooleanField("Is this plan visible to members?", default=True)
    featured = models.BooleanField("Is this plan featured?", default=False)

    def __str__(self):
        return self.name

    def get_object(self):
        plans = []

        for plan in self.plans.filter(visible=True):
            plans.append(plan.get_object())

        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "featured": self.featured,
            "plans": plans,
        }


# This is a Stripe Price
class PaymentPlan(models.Model):
    """A Membership Plan that specifies how a member is billed for a member tier."""

    BILLING_PERIODS = [("Months", "month"), ("Weeks", "week"), ("Days", "days")]

    id = models.AutoField(primary_key=True)
    name = models.CharField("Name", max_length=50)
    stripe_id = models.CharField("Stripe Id", max_length=100, unique=True)
    member_tier = models.ForeignKey(
        MemberTier, on_delete=models.CASCADE, related_name="plans"
    )
    visible = models.BooleanField("Is this plan visible to members?", default=True)
    currency = models.CharField(
        "Three letter ISO currency code.", max_length=3, default="aud"
    )
    cost = models.IntegerField("The cost in cents for this membership plan.")
    interval_count = models.IntegerField(
        "How frequently the price is charged at (per billing interval)."
    )
    interval = models.CharField(choices=BILLING_PERIODS, max_length=10)

    def __str__(self):
        return self.name

    def get_object(self):
        return {
            "id": self.id,
            "name": self.name,
            "currency": self.currency,
            "cost": self.cost,
            "intervalAmount": self.interval_count,
            "interval": self.interval,
        }
