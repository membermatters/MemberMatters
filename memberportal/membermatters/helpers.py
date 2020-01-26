from profile.models import EventLog, UserEventLog


def log_user_event(user, description, event_type, data=""):
    UserEventLog(
        description=description, logtype=event_type,
        user=user, data=data).save()


def log_event(description, event_type, data=""):
    EventLog(description=description, logtype=event_type, data=data).save()
