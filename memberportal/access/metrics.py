from prometheus_client import Counter, Histogram

device_connections_total = Counter(
    "device_connections_total",
    "Number of device connections",
    ["type", "id", "name"],
)

device_disconnections_total = Counter(
    "device_disconnections_total",
    "Number of device disconnections",
    ["type", "id", "name"],
)

device_authentications_total = Counter(
    "device_authentications_total",
    "Number of device authentications",
    ["type", "id", "name"],
)

device_checkins_total = Counter(
    "device_checkins_total",
    "Number of device checkins",
    ["type", "id", "name"],
)

device_access_successes_total = Counter(
    "device_access_successes_total",
    "Number of successful access swipes logged",
    ["type", "id", "name"],
)

device_access_failures_total = Counter(
    "device_access_failures_total",
    "Number of failed access swipes logged",
    ["type", "id", "name"],
)

device_force_reboots_total = Counter(
    "device_force_reboots_total",
    "Number of force reboots",
    ["type", "id", "name"],
)

device_syncs_total = Counter(
    "device_syncs_total",
    "Number of syncs",
    ["type", "id", "name"],
)

device_force_bumps_total = Counter(
    "device_force_bumps_total",
    "Number of force bumps",
    ["type", "id", "name"],
)

device_force_locks_total = Counter(
    "device_force_locks_total",
    "Number of force locks",
    ["type", "id", "name"],
)

device_force_unlocks_total = Counter(
    "device_force_unlocks_total",
    "Number of force unlocks",
    ["type", "id", "name"],
)

device_interlock_session_activations_total = Counter(
    "device_interlock_session_activations_total",
    "Number of interlock session activations",
    ["type", "id", "name"],
)

device_interlock_sessions_left_on_total = Counter(
    "device_interlock_sessions_left_on_total",
    "Number of interlock sessions left on",
    ["type", "id", "name"],
)

device_interlock_sessions_deactivated_total = Counter(
    "device_interlock_sessions_deactivated_total",
    "Number of interlock session deactivations",
    ["type", "id", "name"],
)

device_interlock_sessions_rejected_total = Counter(
    "device_interlock_sessions_rejected_total",
    "Number of interlock session rejections",
    ["type", "id", "name"],
)

device_interlock_sessions_cost_cents = Counter(
    "device_interlock_sessions_cost_cents",
    "Cost of interlock sessions",
    ["type", "id", "name"],
)

device_interlock_session_duration_seconds = Histogram(
    "device_interlock_session_duration_seconds",
    "Duration of interlock sessions",
    ["type", "id", "name"],
)
