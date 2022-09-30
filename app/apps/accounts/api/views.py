from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from app.apps.accounts.api.serializers import DepartamentSerializer
from app.apps.accounts.models import Departament


class DepartamentQuideViewSet(ListAPIView):
    """
           Перечисляет Отделы .
           permission_classes = (IsAuthenticated,)
    """
    queryset = Departament.objects.all()
    serializer_class = DepartamentSerializer
    permission_classes = (IsAuthenticated, )