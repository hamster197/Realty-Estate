
from pathlib import Path
SAIT_KEY = 'django-insecure-%v!sq3ci$8mbrda6-#9=rjsgh_mi^gg@(t$9#95_w7ps01wd+f'

DATABASES_SETTINGS = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': Path(__file__).resolve().parent.parent / 'db.sqlite3',
    }
}

EMAIL_USER = 'hamstertest197@yandex.ru'
EMAIL_PASSWORD = 'Samsung_1978'

BEELINE_TOKEN = 'db73cb07-1624-45ab-8ea2-4decea1db7a0'
BEELINE_COOKIE = 'SRVNAME=AAP'