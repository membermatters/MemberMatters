from django.urls import path
from . import views

urlpatterns = [
    path(
        "api/billing/card/",
        views.MemberBucksAddCard.as_view(),
        name="MemberBucksAddCard",
    ),
    path(
        "api/billing/tiers/",
        views.MemberTiers.as_view(),
        name="MemberTiers",
    ),
    path(
        "api/billing/stripe-webhook/",
        views.StripeWebhook.as_view(),
        name="StripeWebhook",
    ),
]
