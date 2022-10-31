# Realty-Estate
Small crm for estate agency(in development)
# Instalation
1. Create sait_settings.py with settings
SAIT_KEY (SECRET_KEY)
DATABASES_SETTINGS (YOU DATABASES SETTINGS)
EMAIL_USER & EMAIL_PASSWORD (FOR MAILING)
BEELINE_TOKEN & BEELINE_COOKIE
2. pip install -r requirements.txt
3. install redis and start redis-server
4. python manage.py makemigrations
5. python manage.py migrate
6. python manage.py createsuperuser
7. celery -A app worker -l INFO
8. python manage.py runserver
