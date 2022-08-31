
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from rest_framework.serializers import ModelSerializer

from app.apps.accounts.models import Departament


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ('pk',  'last_name', 'first_name',  'patronymic', 'email', 'phone', 'nach_otd', 'departament',
                  'avatar',)


class DepartamentSerializer(ModelSerializer):
    class Meta:
        model = Departament
        fields = '__all__'