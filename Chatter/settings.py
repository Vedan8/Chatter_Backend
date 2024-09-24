import os
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'cdbl44kl@)5k*_$vk$%18aptdu)y-tx@$0mj6dcdx6eq16&ppk' 

DEBUG = True 

import dj_database_url

ALLOWED_HOSTS = ["*"]  

INSTALLED_APPS = [
    "daphne",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'cloudinary',
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist', 
    'core', 
    'corsheaders',
    'chat',
    'post',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Chatter.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request', 
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI_APPLICATION = 'Chatter.wsgi.application'
ASGI_APPLICATION = "Chatter.asgi.application"


DATABASES = {
    'default': dj_database_url.parse("postgresql://chatter_data_6tfg_user:F2aRAep5IlJODNj9pu9cXCigrPPou3si@dpg-crp3fvlds78s73d3s2e0-a.singapore-postgres.render.com/chatter_data_6tfg")
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'  
USE_I18N = True
USE_L10N = True
USE_TZ = True

# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = 'static/'
MEDIA_URL='media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'otpkjaef@gmail.com' 
EMAIL_HOST_PASSWORD = 'djkbolzvzmcyambl'  


# RECAPTCHA_PUBLIC_KEY = '6Ld7yUoqAAAAAOO8-k9JBKDmojafRYjhAZ-zOcl5'    # Replace with your reCAPTCHA public key
# RECAPTCHA_PRIVATE_KEY = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'  # Replace with your reCAPTCHA private key


AUTH_USER_MODEL = 'core.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),  
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),    
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',

    'TOKEN_AUTHENTICATION_CLASS': 'rest_framework_simplejwt.authentication.JWTAuthentication',

    'TOKEN_BLACKLIST_ENABLED': True,
}

CORS_ALLOW_CREDENTIALS: True
CORS_ALLOW_ALL_ORIGINS = True

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [f"redis://:{'TBQWaozZBxxHWiLFmuG1tmf6YySHMb5I'}@redis-15562.c305.ap-south-1-1.ec2.redns.redis-cloud.com:15562"],
        },
    },
}



LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'core': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}


CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dtfo1nvhr',
    'API_KEY': '921286418385759',
    'API_SECRET': 'TXTSpg5xl0m3RbkvLWvHg4frFLw',
    'STATICFILES_MANIFEST_ROOT': os.path.join(BASE_DIR, 'my-manifest-directory')
}

STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticHashedCloudinaryStorage'

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.RawMediaCloudinaryStorage'

