from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("members/list/export", views.member_export, name="member_export"),
    path("api/member/<int:member_id>/xero/add/", views.add_to_xero, name="add_to_xero"),
    path(
        "api/member/<int:member_id>/xero/create_invoice/",
        views.create_invoice,
        name="create_invoice",
    ),
    path(
        "api/member/<int:member_id>/xero/create_invoice/<str:option>/",
        views.create_invoice,
        name="create_invoice",
    ),
    path("api/members/xero/sync", views.sync_xero_accounts, name="sync_xero_accounts"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
