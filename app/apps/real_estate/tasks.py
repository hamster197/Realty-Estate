from app.apps.real_estate.models import RealtyEstateGalery
from app.celery import app
from django.shortcuts import get_object_or_404

@app.task
def galery_watermak(galery_ids):
    for instance in galery_ids:
        get_object_or_404(RealtyEstateGalery, pk=instance).save()
