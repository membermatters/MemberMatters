from prometheus_client import Gauge

member_count_total = Gauge(
    "member_count_total",
    "Number of members in the system",
    ["state"],
)

subscription_count_total = Gauge(
    "subscription_count_total",
    "Number of subscriptions in the system",
    ["status"],
)
