import os

DJANGO_KEY = os.getenv('DJANGO_KEY')

POSTGRES_DB = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'Autosaloon_db',
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASS'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        }
    }


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
