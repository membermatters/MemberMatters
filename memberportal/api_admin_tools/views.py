from profile.models import User
from access import models
from .models import MemberTier, PaymentPlan
from constance import config
from services.emails import send_single_email
import json
import stripe

stripe.api_key = config.STRIPE_SECRET_KEY

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
                    {
                        "success": True,
                        "message": "adminTools.makeMemberSuccess",
                    }
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
                    {
                        "success": False,
                        "message": "adminTools.makeMemberError",
                    }
                )
        else:
            return Response(
                {
                    "success": False,
                    "message": "adminTools.makeMemberErrorExists",
                }
            )


class Doors(APIView):
    """
    get: returns a list of doors.
    put: updates a specific door.
    delete: deletes a specific door.
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

    def put(self, request, door_id):
        door = models.Doors.objects.get(pk=door_id)

        data = request.data

        door.name = data.get("name")
        door.description = data.get("description")
        door.ip_address = data.get("ipAddress")

        door.all_members = data.get("defaultAccess")
        door.locked_out = data.get("maintenanceLockout")
        door.play_theme = data.get("playThemeOnSwipe")
        door.exempt_signin = data.get("exemptFromSignin")
        door.hidden = data.get("hiddenToMembers")

        door.save()

        return Response()

    def delete(self, request, door_id):
        door = models.Doors.objects.get(pk=door_id)
        door.delete()

        return Response()


class Interlocks(APIView):
    """
    get: returns a list of interlocks.
    put: update a specific interlock.
    delete: delete a specific interlock.
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

        interlock.name = data.get("name")
        interlock.description = data.get("description")
        interlock.ip_address = data.get("ipAddress")

        interlock.all_members = data.get("defaultAccess")
        interlock.locked_out = data.get("maintenanceLockout")
        interlock.play_theme = data.get("playThemeOnSwipe")
        interlock.exempt_signin = data.get("exemptFromSignin")
        interlock.hidden = data.get("hiddenToMembers")

        interlock.save()

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
    post: This method sends a welcome email to the specified member.
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


class MemberTiers(APIView):
    """
    get: gets a list of all member tiers.
    post: creates a new member tier.
    put: updates a new member tier.
    delete: a member tier.
    """

    permission_classes = (permissions.IsAdminUser,)

    def get(self, request):
        tiers = MemberTier.objects.all()
        formatted_tiers = []

        for tier in tiers:
            formatted_tiers.append(
                {
                    "id": tier.id,
                    "name": tier.name,
                    "description": tier.description,
                    "visible": tier.visible,
                    "featured": tier.featured,
                }
            )

        return Response(formatted_tiers)

    def post(self, request):
        body = request.data
        product = stripe.Product.create(
            name=body["name"], description=body["description"]
        )
        tier = MemberTier.objects.create(
            name=body["name"],
            description=body["description"],
            visible=body["visible"],
            featured=body["featured"],
            stripe_id=product.id,
        )

        return Response()

    def delete(self, request):
        return Response()


class ManageMemberTier(APIView):
    """
    get: gets a member tier.
    put: updates a member tier.
    delete: deletes a member tier.
    """

    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, tier_id):
        body = request.data

        try:
            tier = MemberTier.objects.get(pk=tier_id)

        except MemberTier.DoesNotExist as e:
            return Response(status=status.HTTP_404_NOT_FOUND)

        formatted_tier = {
            "id": tier.id,
            "name": tier.name,
            "description": tier.description,
            "visible": tier.visible,
            "featured": tier.featured,
        }

        return Response(formatted_tier)

    def put(self, request, tier_id):
        body = request.data

        tier = MemberTier.objects.get(pk=tier_id)

        tier.name = body["name"]
        tier.description = body["description"]
        tier.visible = body["visible"]
        tier.featured = body["featured"]
        tier.save()

        return Response()

    def delete(self, request, tier_id):
        tier = MemberTier.objects.get(pk=tier_id)
        tier.delete()

        return Response()


class ManageMemberTierPlans(APIView):
    """
    post: creates a new member tier plan.
    """

    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, tier_id):
        plans = PaymentPlan.objects.filter(member_tier=tier_id)
        formatted_plans = []

        for plan in plans:
            formatted_plans.append(
                {
                    "id": plan.id,
                    "name": plan.name,
                    "stripeId": plan.stripe_id,
                    "memberTier": plan.member_tier.id,
                    "visible": plan.visible,
                    "currency": plan.currency,
                    "cost": plan.cost / 100,  # convert to dollars
                    "intervalCount": plan.interval_count,
                    "interval": plan.interval,
                }
            )

        return Response(formatted_plans)

    def post(self, request, tier_id=None):
        if tier_id is not None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        body = request.data

        member_tier = MemberTier.objects.get(pk=body["memberTier"])

        stripe_plan = stripe.Price.create(
            unit_amount=body["cost"],
            currency=str(body["currency"]).lower(),
            recurring={
                "interval": body["interval"],
                "interval_count": body["intervalCount"],
            },
            product=member_tier.stripe_id,
        )

        PaymentPlan.objects.create(
            name=body["name"],
            stripe_id=stripe_plan.id,
            member_tier_id=body["memberTier"],
            visible=body["visible"],
            currency=str(body["currency"]).lower(),
            cost=int(body["cost"]),
            interval_count=body["intervalCount"],
            interval=body["interval"],
        )

        return Response()


class ManageMemberTierPlan(APIView):
    """
    get: gets a member tier plan.
    put: updates a member tier plan.
    delete: deletes a member tier plan.
    """

    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, plan_id):
        body = request.data

        plan = PaymentPlan.objects.get(pk=plan_id)

        formatted_plan = {
            "id": plan.id,
            "name": plan.name,
            "member_tier": plan.member_tier,
            "visible": plan.visible,
            "cost": plan.cost,
            "interval_count": plan.interval_count,
            "interval": plan.interval,
        }

        return Response(formatted_plan)

    def put(self, request, plan_id):
        body = request.data

        plan = PaymentPlan.objects.get(pk=plan_id)

        plan.name = body["name"]
        plan.visible = body["visible"]
        plan.cost = body["cost"]
        plan.save()

        return Response()

    def delete(self, request, plan_id):
        plan = PaymentPlan.objects.get(pk=plan_id)
        plan.delete()

        return Response()
