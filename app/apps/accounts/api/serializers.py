from django.contrib.auth.models import Group
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers

from app.apps.accounts.models import Departament, MyUser
from app.apps.real_estate.models import CityQuide, DistrictQuide


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ('pk',  'last_name', 'first_name',  'patronymic', 'email', 'phone', 'department_boss', 'departament',
                  'avatar', 'groups',)

class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class CitySerializer(ModelSerializer):
    class Meta:
        model = CityQuide
        fields = '__all__'

class DepartamentSerializer(ModelSerializer):
    class Meta:
        model = Departament
        fields = '__all__'

class DistrictSerializer(ModelSerializer):
    class Meta:
        model = DistrictQuide
        fields = '__all__'

class SubjectTransferSerializer(Serializer):
    users_list = []
    for user in MyUser.objects.all():
        users_list.append(user.pk)
    user_from = serializers.ChoiceField(users_list)
    user_to = serializers.ChoiceField(users_list)

    def validate(self, validated_data):
        if validated_data['user_from'] == validated_data['user_to']:
            raise serializers.ValidationError(' - Error: user_from and user_to cant be equeal')
        else:
            return validated_data

