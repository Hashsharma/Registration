from rest_framework import serializers

from User.models import RegistrationModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationModel
        fields = '__all__'
