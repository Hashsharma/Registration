from rest_framework import serializers

from User.models import UserRegistrationModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRegistrationModel
        fields = '__all__'
