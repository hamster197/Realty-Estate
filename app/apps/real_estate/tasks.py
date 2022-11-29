from celery import shared_task

from app.apps.real_estate.models import RealtyEstateGalery, RealtyEstate
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
    instance = get_object_or_404(RealtyEstate, pk=instance_pk)
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

