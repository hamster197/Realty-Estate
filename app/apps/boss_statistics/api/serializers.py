from rest_framework import serializers
from rest_framework.serializers import Serializer

from app.apps.real_estate.models import DistrictQuide


class InstatnseStatisticSerializer(Serializer):
    pk = serializers.IntegerField()
    not_contract_realtys_all = serializers.IntegerField()
    not_contract_realtys_new = serializers.IntegerField()
    contract_realtys_all = serializers.IntegerField()
    contract_realtys_new = serializers.IntegerField()
    open_deals_sum = serializers.FloatField()
    open_deals_count = serializers.IntegerField()
    close_deals_sum= serializers.FloatField()
    close_deals_count = serializers.IntegerField()

class InstatnseReitingSerializer(Serializer):
    pk = serializers.IntegerField()

class RealtyEstateSerializer(Serializer):
    pk = serializers.IntegerField()
    creation_date = serializers.DateField()
    type = serializers.CharField()
    contract = serializers.CharField()
    district = serializers.CharField()
    agency_price = serializers.FloatField()

class ClientSerializer(Serializer):
    pk = serializers.IntegerField()
    creation_date =serializers.DateField()
    client_name = serializers.CharField()
    district = serializers.PrimaryKeyRelatedField(queryset=DistrictQuide.objects.all(), many=True)
    max_price = serializers.FloatField()
