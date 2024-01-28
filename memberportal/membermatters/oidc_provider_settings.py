def userinfo(claims, user):
    # Populate claims dict.
    claims["name"] = user.get_full_name() or "NO_NAME"
    claims["given_name"] = user.profile.first_name or "NO_FIRSTNAME"
    claims["family_name"] = user.profile.last_name or "NO_LASTNAME"
    claims["nickname"] = user.profile.screen_name or "NO_SCREENNAME"
    claims["preferred_username"] = user.profile.screen_name or "NO_SCREENNAME"
    claims["email"] = user.email
    claims["email_verified"] = user.email_verified
    claims["phone_number"] = user.profile.phone or "NO_PHONENUMBER"
    claims["phone_number_verified"] = False
    claims["updated_at"] = user.profile.modified.isoformat()

    return claims


from django.utils.translation import ugettext_lazy as _
from oidc_provider.lib.claims import ScopeClaims


class CustomScopeClaims(ScopeClaims):
    info_membershipinfo = (
        _("Membership Info"),
        _(
            "Current membership status, and other membership information like permissions/groups."
        ),
    )

    def scope_membershipinfo(self):
        groups = []
        state = self.user.profile.state
        subscription_state = self.user.profile.subscription_state
        subscriptionActive = subscription_state in ["active", "cancelling"]
        firstSubscribed = self.user.profile.subscription_first_created
        firstSubscribed = firstSubscribed.isoformat() if firstSubscribed else None

        if self.user.is_staff:
            groups.append("staff")

        if self.user.is_admin:
            groups.append("admin")

        if self.user.is_superuser:
            groups.append("superuser")

        if self.user.profile.state == "active":
            groups.append("active")

        return {
            "state": state,
            "active": state == "active",
            "subscriptionState": subscription_state,
            "subscriptionActive": subscriptionActive,
            "firstSubscribedDate": firstSubscribed,
            "groups": groups,
        }
