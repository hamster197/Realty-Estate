# Realty-Estate
Small crm for estate agency(in development)
# Instalation
1. Create .env with settings
SAIT_KEY (SECRET_KEY)
ALLOWED_HOSTS and INTERNAL_IPS (YOU HOST & IP)
EMAIL_USER & EMAIL_PASSWORD (FOR MAILING)
BEELINE_TOKEN & BEELINE_COOKIE
DATABASE_ENGINE & DATABASE_NAME
CACHEOPS_REDIS & REDIS_HOST , REDIS_PORT
2. pip install -r requirements.txt
3. install redis and start redis-server
4. python manage.py makemigrations
5. python manage.py migrate
6. python manage.py createsuperuser
7. celery -A app worker -l INFO
8. python manage.py runserver

 https://deepwiki.com/hamster197/Realty-Estate/2.3-client-management
