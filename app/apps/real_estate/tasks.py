from celery import shared_task

from app.apps.real_estate.models import RealtyEstateGalery, RealtyEstate, Flat
from app.celery import app
from django.shortcuts import get_object_or_404

from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@app.task
def galery_watermak(galery_ids):
    for instance in galery_ids:
        get_object_or_404(RealtyEstateGalery, pk=instance).save()

@shared_task(bind=True,)
def get_adress(self, instance_pk):
    instance = RealtyEstate.objects.nocache().get(pk=instance_pk)
    from geopy.geocoders import Nominatim
    geolocator = Nominatim(user_agent='realty-test-app')
    try:
        location = geolocator.geocode(instance.district.city.name + ' ' + instance.street + ' ' + instance.street_number,
                                      timeout=10)
        if location:
            instance.latitude = location.latitude
            instance.longitude = location.longitude
            instance.save()

    except Exception as e:
        raise self.retry(exc=e, countdown=5)

@shared_task(bind=True)
def get_cadastral_number(self, instance_pk):
    try:
        instance = RealtyEstate.objects.nocache().get(pk=instance_pk)
        import requests
        url = 'http://rosreestr.ru/api/online/address/fir_objects?macroRegionId=103000000000&RegionId='\
              + instance.district.city.cadastral_region_id
        url = url + '&street=' + instance.street + '&house=' +instance.street_number
        if instance.type=='Квартира':
            flat = get_object_or_404(Flat, pk=instance_pk)
            if flat.flat_number:
                url = url + '&apartment=' + flat.flat_number
        payload = {}
        headers = {'User-Agent': 'My User Agent 1.0', }
        response = requests.request("GET", url, headers=headers, data=payload, verify=False, )
        if response.status_code==200:
            cadastral_number = ''
            for i in response.json():
                if str(i['regionId'])==instance.district.city.cadastral_region_id:
                    cadastral_number = str(i['objectCn'])
            instance.cadastral_number = cadastral_number
            instance.save()

    except Exception as e:
        raise self.retry(exc=e, countdown=5)
