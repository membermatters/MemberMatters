from profile.models import User
from group.models import Group
from access import models
from constance import config
from profile.emailhelpers import send_single_email
import requests

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


class GetMembers(APIView):
    """
    get: This method returns a list of members.
    """

    permission_classes = (permissions.IsAdminUser,)

    def get(self, request):
        members = User.objects.all()

        def get_member(user):
            profile = user.profile

            return {
                "id": user.id,
                "admin": user.is_staff,
                "superuser": user.is_admin,
                "email": user.email,
                "registrationDate": profile.created,
                "lastUpdatedProfile": profile.modified,
                "screenName": profile.screen_name,
                "name": {
                    "first": profile.first_name,
                    "last": profile.last_name,
                    "full": profile.get_full_name(),
                },
                "phone": profile.phone,
                "state": profile.get_state_display(),
                # "picture": picture,
                "memberType": {
                    "name": profile.member_type.name,
                    "id": profile.member_type_id,
                },
                "groups": profile.groups.all().values(),
                "rfid": profile.rfid,
                # "access": {
                #     "doors": profile.doors.all().values(),
                #     "interlocks": profile.interlocks.all().values(),
                # },
                # "memberBucks": {
                #     "balance": profile.memberbucks_balance,
                #     "lastPurchase": profile.last_memberbucks_purchase,
                # },
                "updateProfileRequired": profile.must_update_profile,
                # "last_seen": profile.last_seen,
                # "last_induction": profile.last_induction,
                # "stripe": {
                #     "cardExpiry": profile.stripe_card_expiry,
                #     "last4": profile.stripe_card_last_digits,
                # },
                # "xero": {
                #     "accountId": profile.xero_account_id,
                #     "accountNumber": profile.xero_account_number,
                # },
            }

        return Response(map(get_member, members))


class MemberState(APIView):
    """
    get: This method gets a member's state.
    post: This method sets a member's state.
    """

    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, member_id, state=None):
        member = User.objects.get(id=member_id)

        return Response({"state": member.profile.state})

    def post(self, request, member_id, state):
        member = User.objects.get(id=member_id)
        if state == "active":
            member.profile.activate(request)
        elif state == "inactive":
            member.profile.deactivate(request)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response()


class MakeMember(APIView):
    """
    post: This activates a new member.
    """

    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, member_id):
        user = User.objects.get(id=member_id)
        if user.profile.state == "noob":
            # give default door access
            for door in models.Doors.objects.filter(all_members=True):
                user.profile.doors.add(door)

            # give default interlock access
            for interlock in models.Interlock.objects.filter(all_members=True):
                user.profile.interlocks.add(interlock)

            email = user.email_welcome()
            xero = user.profile.add_to_xero()
            invoice = user.profile.create_membership_invoice()
            user.profile.state = (
                "inactive"  # an admin should activate them when they pay their invoice
            )
            user.profile.save()

            if "Error" not in xero and "Error" not in invoice and email:
                return Response(
                    {
                        "success": True,
                        "message": "Successfully added to Xero and sent welcome email.",
                    }
                )

            elif "Error" in xero:
                return Response({"success": False, "message": xero})

            elif "Error" in invoice:
                return Response({"success": False, "message": invoice})

            elif email is False:
                return Response(
                    {"success": False, "message": "Error, couldn't send welcome email."}
                )

            else:
                return Response(
                    {
                        "success": False,
                        "message": "Unknown error while making into member.",
                    }
                )

        return Response(status=status.HTTP_400_BAD_REQUEST)


class Doors(APIView):
    """
    get: This method returns a list of doors.
    """

    permission_classes = (permissions.IsAdminUser,)

    def get(self, request):
        doors = models.Doors.objects.all()

        def get_door(door):
            return {
                "name": door.name,
                "lastSeen": door.last_seen,
                "ipAddress": door.ip_address,
            }

        return Response(map(get_door, doors))


class Interlocks(APIView):
    """
    get: This method returns a list of interlocks.
    """

    permission_classes = (permissions.IsAdminUser,)

    def get(self, request):
        interlocks = models.Interlock.objects.all()

        def get_door(interlock):
            return {
                "name": interlock.name,
                "lastSeen": interlock.last_seen,
                "ipAddress": interlock.ip_address,
            }

        return Response(map(get_door, interlocks))
