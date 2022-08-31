from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from app.apps.real_estate.models import Flat, House, PlotOfLand, Commerce, RealtyEstateGalery, RealtyEstate, \
    DistrictQuide, CityQuide, Client


class CityQuideSerializer(serializers.ModelSerializer):

    class Meta:
        model = CityQuide
        fields = '__all__'

class DistrictQuideSerializer(serializers.ModelSerializer):

    class Meta:
        model = DistrictQuide
        fields = '__all__'

class AllRealtySerializer(serializers.ModelSerializer):

    class Meta:
        model = RealtyEstate
        exclude = ['client_name', 'client_tel', 'latitude', 'longitude',]

class RealtySerializer(ModelSerializer):
    galery_real_estate_id = serializers.SerializerMethodField('get_image_url',)

    def get_image_url(self, obj):
        request = self.context.get("request")
        galery =[]
        for image in obj.galery_real_estate_id.all():
            galery.append(request.build_absolute_uri(image))
        return galery

    class Meta:
        model = RealtyEstate
        exclude = ['author', 'latitude', 'longitude',]

class MyFlatsSerializer(RealtySerializer):
    class Meta(RealtySerializer.Meta):
        model = Flat

class MyHousesSerializer(RealtySerializer):
    class Meta(RealtySerializer.Meta):
        model = House

class MyPlotOfLandsSerializer(RealtySerializer):
    class Meta(RealtySerializer.Meta):
        model = PlotOfLand

class MyCommercesSerializer(RealtySerializer):
    class Meta(RealtySerializer.Meta):
        model = Commerce

class RealtyEstateGalerySerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = RealtyEstateGalery
        fields = ['pk','realty_estate', 'image', ]

    def validate(self, validated_data):
        if not RealtyEstate.objects.filter(pk=str(validated_data.get('realty_estate')),
                                           author=self.context['request'].user).exists():
            raise serializers.ValidationError('You must be author of realty estate instance')
        else:
            return validated_data

class MyClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        exclude = ['author']

class AllClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        exclude = ['client_name', 'phone', 'email',]

