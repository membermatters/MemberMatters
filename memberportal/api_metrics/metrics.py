from prometheus_client import Gauge

member_count_total = Gauge(
    "mm_member_count_total",
    "Number of members in the system",
    ["state"],
)

subscription_count_total = Gauge(
    "mm_subscription_count_total",
    "Number of subscriptions in the system",
    ["state"],
)
