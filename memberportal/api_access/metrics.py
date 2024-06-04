from prometheus_client import Gauge

devices_total = Gauge(
    "mm_devices_total",
    "Number of devices",
    ["type"],
)

devices_online_total = Gauge(
    "mm_devices_online_total",
    "Number of online devices",
    ["type"],
)

devices_offline_total = Gauge(
    "mm_devices_offline_total",
    "Number of offline devices",
    ["type"],
)

devices_locked_out_total = Gauge(
    "mm_devices_locked_out_total",
    "Number of locked out devices",
    ["type"],
)
