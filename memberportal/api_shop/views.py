from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.views import APIView
from constance import config
from .models import Product, Category, Supplier, Transaction
from profile.models import Profile
from api_general.models import SiteSession
import json


class AllProducts(APIView):
    """Returns the details for a specific product"""

    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        return Response()


class ProductDetail(APIView):
    """Returns the details for a specific product"""

    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        return Response()
