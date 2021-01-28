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
        "api/billing/plans/<int:plan_id>/signup/",
        views.PaymentPlanSignup.as_view(),
        name="PaymentPlanSignup",
    ),
    path(
        "api/billing/myplan/<str:resume>/",
        views.PaymentPlanResumeCancel.as_view(),
        name="PaymentPlanResumeCancel",
    ),
    path(
        "api/billing/myplan/",
        views.SubscriptionInfo.as_view(),
        name="SubscriptionInfo",
    ),
    path(
        "api/billing/can-signup/",
        views.CanSignup.as_view(),
        name="CanSignup",
    ),
    path(
        "api/billing/check-induction/",
        views.CheckInductionStatus.as_view(),
        name="CheckInductionStatus",
    ),
    path(
        "api/billing/stripe-webhook/",
        views.StripeWebhook.as_view(),
        name="StripeWebhook",
    ),
]
