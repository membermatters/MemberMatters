from django.http import (
    HttpResponse,
    JsonResponse,
)
from django.contrib.auth.decorators import login_required
from membermatters.decorators import staff_required
from membermatters.helpers import log_user_event
from .models import Profile, User
import pytz
import csv

utc = pytz.UTC

permission_message = "You are not authorised to do that."


@login_required
@staff_required
def member_export(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="memberlist.csv"'
    members = Profile.objects.prefetch_related("user")

    writer = csv.writer(response)
    writer.writerow(["first_name", "last_name", "email", "status"])

    for member in members:
        writer.writerow([member.first_name, member.last_name, member, member.state])

    return response


@login_required
@staff_required
def sync_xero_accounts(request):
    from .xerohelpers import sync_xero_accounts

    success = sync_xero_accounts(User.objects.all().prefetch_related())
    log_user_event(request.user, "Resynced xero accounts.", "profile")

    if success:
        return JsonResponse({"message": success})

    else:
        return JsonResponse({"message": "Couldn't sync xero accounts, unknown error."})


@login_required
@staff_required
def add_to_xero(request, member_id):
    return JsonResponse(
        {"message": User.objects.get(pk=member_id).profile.add_to_xero()}
    )


@login_required
def create_invoice(request, member_id, option=False):
    email_invoice = False

    if "email" == option:
        email_invoice = True

    if request.user.profile.can_generate_invoice:
        response = User.objects.get(pk=member_id).profile.create_membership_invoice(
            email_invoice=email_invoice
        )

        return JsonResponse({"message": response})

    else:
        return JsonResponse({"message": permission_message})
