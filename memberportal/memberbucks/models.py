from django.core.validators import URLValidator
from django.db import models
from django.conf import settings
from django.db.models import Sum
from django.utils import timezone
from django_prometheus.models import ExportModelOperationsMixin


class MemberBucks(ExportModelOperationsMixin("memberbucks"), models.Model):
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
    description = models.CharField("Description of Transaction", max_length=500)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    logging_info = models.TextField("Detailed logging info from stripe.", blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} {'debited' if self.amount < 0 else 'credited'} ${abs(self.amount)} for {self.description} on {self.date.date()}"

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


class MemberbucksProduct(
    ExportModelOperationsMixin("memberbucks-products"), models.Model
):
    """A new Memberbucks product should be created for each vending machine if you want to use the stock
    tracking or reporting features, or their external_id is different."""

    def __str__(self):
        return f"{self.name} ({self.external_id_name})"

    id = models.AutoField(primary_key=True)
    name = models.CharField("Name", max_length=30, unique=False)
    description = models.CharField(
        "Description of product", max_length=250, null=True, blank=True
    )
    image_url = models.TextField(
        "Product image", null=True, blank=True, validators=[URLValidator()]
    )

    # These two are separate fields, but may be the same value.
    # We split them for flexibility, for example, MDB reports product IDs numerically but most vending
    # machines will use A0, A1, B0, B1, etc. on customer facing labels.
    external_id = models.CharField("External ID", max_length=250, null=True, blank=True)
    external_id_name = models.CharField(
        "External ID human-readable name", max_length=250, null=True, blank=True
    )

    stock_level = models.IntegerField(
        "Number of this product left and available to dispense.", default=0
    )
    price = models.IntegerField("Price in cents to be charged to the end user.")
    cost_price = models.IntegerField(
        "Price in cents that it costs to buy this product."
    )  # (used for profit estimates)


class MemberbucksProductPurchaseLog(
    ExportModelOperationsMixin("memberbucks-product-purchase-log"), models.Model
):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(MemberbucksProduct, on_delete=models.CASCADE)
    memberbucks_device = models.ForeignKey(
        "access.MemberbucksDevice", on_delete=models.CASCADE
    )
    date = models.DateTimeField(default=timezone.now)
    price = models.IntegerField("Price in cents that was charged to the end user.")
    cost_price = models.IntegerField(
        "Price in cents that it costs to buy this product."
    )  # (used for profit estimates)
    success = models.BooleanField(default=True)

    def __str__(self):
        success_string = "bought" if self.success else "tried unsuccessfully to buy"
        return f"{self.user.get_full_name()} ({self.user.profile.screen_name}) {success_string} a {self.product.name} at {self.date.date()}"
