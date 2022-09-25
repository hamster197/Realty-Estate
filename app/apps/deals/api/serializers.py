from rest_framework.relations import StringRelatedField
from rest_framework.serializers import ModelSerializer

from app.apps.deals.models import Deal, SalesChanelQuide, RealtorInTheDeal, SubmittedCommission


class SalesChanelQuideSerializer(ModelSerializer):
    class Meta:
        model = SalesChanelQuide
        fields = '__all__'

class DealSerializer(ModelSerializer):
    realtor_in_deal_deal_id = StringRelatedField(many=True, read_only=True)
    commision_deal_id = StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Deal
        exclude = ('status',)

class DealIsBossSerializer(ModelSerializer):

    class Meta:
        model = Deal
        fields = '__all__'

class DealRealtorsSerializer(ModelSerializer):

    class Meta:
        model = RealtorInTheDeal
        exclude = ('realtor_commision_sum',)

class SubmittedCommissionSerializer(ModelSerializer):

    class Meta:
        model = SubmittedCommission
        exclude = ('commission_date',)

class DealReitingSerializer(ModelSerializer):
    name = StringRelatedField()

    class Meta:
        depth = 1
        model = RealtorInTheDeal
        exclude = ('id', 'percent', 'deal', )

    def __init__(self, *args, **kwargs):
        super(DealReitingSerializer, self).__init__(*args, **kwargs)
        if self.context['request'].user.groups.get().name == 'Риелтор':
            self.Meta.exclude = ['id', 'percent', 'deal','realtor_commision_sum']





