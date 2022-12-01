from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

from app.settings import BASE_DIR
import os
from PIL import Image

from app.apps.real_estate.models import Flat, House, PlotOfLand, Commerce, RealtyEstateGalery, RealtyEstate


def save_all_watermark(self):
    crm_watermark = os.path.join(BASE_DIR, 'static') + '/logo21.png'
    if os.path.exists(crm_watermark):
        filepath = self.image.path
        image = Image.open(filepath).convert('RGB')
        a1 = round(image.size[0] / 2)
        watermark = Image.open(crm_watermark).resize((a1, a1))

        image.paste(watermark, (round(image.size[0] / 2) - round(a1 / 2), round(image.size[1] / 2) - round(a1 / 2)),
                    watermark)
        image.save(filepath)


@receiver(post_save, sender=Flat)
@receiver(post_save, sender=House)
@receiver(post_save, sender=PlotOfLand)
@receiver(post_save, sender=Commerce)
def update_main_image(instance, **kwargs):

    from .tasks import get_adress, get_cadastral_number
    get_cadastral_number.apply_async(args=(instance.pk,), countdown=10)
    get_adress.apply_async(args=(instance.pk,), countdown=10)
    save_all_watermark(instance)

@receiver(post_save, sender=RealtyEstateGalery)
def update_galery_image(instance, **kwargs):
    save_all_watermark(instance)


