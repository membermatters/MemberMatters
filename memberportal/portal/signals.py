from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone

@receiver(user_logged_in)
def sig_user_logged_in(sender, user, request, **kwargs):
    user.profile.last_seen = timezone.now()
    user.profile.save()