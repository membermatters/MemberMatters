from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from profile.models import User, Profile, MemberTypes


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("first_name", "last_name")


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ("id", "email", "profile")
