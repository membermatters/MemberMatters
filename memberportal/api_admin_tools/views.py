from profile.models import User
from access import models
from constance import config
from profile.emailhelpers import send_single_email
import json

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
        members = User.objects.select_related("profile", "profile__member_type").all()

        filtered = []

        for member in members:
            filtered.append(member.profile.get_basic_profile())

        return Response(filtered)


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
            user.profile.update_last_induction()
            user.profile.save()

            subject = f"{user.profile.get_full_name()} just got turned into a member!"
            send_single_email(
                request.user, config.EMAIL_ADMIN, subject, subject, subject
            )

            if "Error" not in xero and "Error" not in invoice and email:
                return Response(
                    {"success": True, "message": "adminTools.makeMemberSuccess",}
                )

            elif "Error" in xero:
                return Response({"success": False, "message": xero})

            elif "Error" in invoice:
                return Response({"success": False, "message": invoice})

            elif email is False:
                return Response(
                    {"success": False, "message": "adminTools.makeMemberErrorEmail"}
                )

            else:
                return Response(
                    {"success": False, "message": "adminTools.makeMemberError",}
                )
        else:
            return Response(
                {"success": False, "message": "adminTools.makeMemberErrorExists",}
            )


class Doors(APIView):
    """
    get: This method returns a list of doors.
    """

    permission_classes = (permissions.IsAdminUser,)

    def get(self, request):
        doors = models.Doors.objects.all()

        def get_door(door):
            return {
                "id": door.id,
                "name": door.name,
                "description": door.description,
                "ipAddress": door.ip_address,
                "lastSeen": door.last_seen,
                "defaultAccess": door.all_members,
                "maintenanceLockout": door.locked_out,
                "playThemeOnSwipe": door.play_theme,
                "exemptFromSignin": door.exempt_signin,
                "hiddenToMembers": door.hidden,
            }

        return Response(map(get_door, doors))
    
    def delete(self, request, door_id):
        door = models.Doors.objects.get(pk=door_id)
        door.delete()

        return Response()


class Interlocks(APIView):
    """
    get: This method returns a list of interlocks.
    """

    permission_classes = (permissions.IsAdminUser,)

    def get(self, request):
        interlocks = models.Interlock.objects.all()

        def get_interlock(interlock):
            return {
                "id": interlock.id,
                "name": interlock.name,
                "description": interlock.description,
                "ipAddress": interlock.ip_address,
                "lastSeen": interlock.last_seen,
                "defaultAccess": interlock.all_members,
                "maintenanceLockout": interlock.locked_out,
                "playThemeOnSwipe": interlock.play_theme,
                "exemptFromSignin": interlock.exempt_signin,
                "hiddenToMembers": interlock.hidden,
            }

        return Response(map(get_interlock, interlocks))
    
    def put(self, request, interlock_id):
        interlock = models.Interlock.objects.get(pk=interlock_id)

        data = request.data
        
        interlock.name = data.name
        
        return Response()
    
    def delete(self, request, interlock_id):
        interlock = models.Interlock.objects.get(pk=interlock_id)
        interlock.delete()
        
        return Response()


class MemberAccess(APIView):
    """
    get: This method gets a member's access permissions.
    """

    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, member_id):
        member = User.objects.get(id=member_id)

        return Response(member.profile.get_access_permissions())


class MemberWelcomeEmail(APIView):
    """
    get: This method sends a welcome email to the specified member.
    """

    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, member_id):
        member = User.objects.get(id=member_id)
        member.email_welcome()

        return Response()


class MemberProfile(APIView):
    """
    put: This method updates a member's profile.
    """

    permission_classes = (permissions.IsAdminUser,)

    def put(self, request, member_id):
        if not member_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        body = json.loads(request.body)
        member = User.objects.get(id=member_id)

        member.email = body.get("email")
        member.profile.first_name = body.get("firstName")
        member.profile.last_name = body.get("lastName")
        member.profile.rfid = body.get("rfidCard")
        member.profile.phone = body.get("phone")
        member.profile.screen_name = body.get("screenName")
        member.profile.member_type_id = body.get("memberType")["id"]

        groups = []

        for x in body.get("groups"):
            groups.append(x["id"])

        member.profile.groups.set(groups)

        member.save()
        member.profile.save()

        return Response()


class MemberCreateNewInvoice(APIView):
    """
    get: This method creates a new invoice for the specified member.
    """

    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, member_id, send_email):
        User.objects.get(pk=member_id).profile.create_membership_invoice(
            email_invoice=send_email == "true"
        )

        return Response()

