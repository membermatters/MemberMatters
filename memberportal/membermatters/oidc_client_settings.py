import logging
from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from profile.models import Profile, User

logger = logging.getLogger("mozilla_django_oidc")


class CustomOIDCAB(OIDCAuthenticationBackend):
    # Given the claims field from the Idp, match to a user by their email address (or None if not found)
    def filter_users_by_claims(self, claims):

        email = claims.get("email")
        logger.debug('Got filter on claim for "{}"\nclaims: {}'.format(email, claims))
        if not email:
            return self.UserModel.objects.none()

        try:
            user = User.objects.get(email=email)
            logger.debug("Found!")
            return [user]
        except User.DoesNotExist:
            logger.debug("Not found")
            return self.UserModel.objects.none()

    # If OIDC_CREATE_USER is set to True and a corresponding user was not found in the Django DB, create a user and profile using the Idp claims
    def create_user(self, claims):
        email = claims.get("email")
        logger.debug('Got a create request for "{}"\nclaims: {}'.format(email, claims))
        is_admin = "admin" in claims.get("groups", [])
        user = User.objects.create(
            email=email.lower(),
            email_verified=True,
            staff=is_admin,
            admin=is_admin,
            is_superuser=is_admin,
        )
        # intentionally not setting a password - assuming that admins can bootstrap if they need local login in the event Idp is offline
        user.save()

        profile = Profile.objects.create(
            user=user,
            first_name=claims.get("given_name") or "NO_FIRSTNAME",
            last_name=claims.get("family_name") or "NO_LASTNAME",
            screen_name=claims.get("preferred_username") or "NO_SCREENNAME",
            phone=claims.get("phone_number") or "NO_PHONE",
            vehicle_registration_plate="",
        )
        profile.save()
        return user

    # If OIDC_CREATE_USER is set to True and a corresponding user was found in the Django DB, update the user and profile records to be current with the claims from the Idp
    def update_user(self, user, claims):
        email = claims.get("email")
        logger.debug('Got a update request for "{}"\nclaims: {}'.format(email, claims))
        is_admin = "admin" in claims.get("groups", [])

        user.email_verified = claims.get("email_verified")
        user.staff = is_admin
        user.admin = is_admin
        user.is_superuser = is_admin
        user.save()

        profile = user.profile
        profile.first_name = claims.get("given_name") or "NO_FIRSTNAME"
        profile.last_name = claims.get("family_name") or "NO_LASTNAME"
        profile.screen_name = claims.get("preferred_username") or "NO_SCREENNAME"
        profile.phone = claims.get("phone_number") or "NO_PHONE"
        profile.save()

        return user
