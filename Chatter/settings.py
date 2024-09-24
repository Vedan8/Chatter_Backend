import os
from pathlib import Path
import dj_database_url
from datetime import timedelta

# Define the base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret key for the Django project
SECRET_KEY = 'cdbl44kl@)5k*_$vk$%18aptdu)y-tx@$0mj6dcdx6eq16&ppk' 

# Debug mode
DEBUG = True

# Allowed hosts
ALLOWED_HOSTS = ["*"]

# Installed apps
INSTALLED_APPS = [
    "daphne",  # For handling ASGI and WebSocket connections
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
    'core',  # Your core app containing the User model
    'corsheaders',
    'chat',  # Your chat app
    'post',  # Another app for posts
]

# Middleware configuration
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL configuration
ROOT_URLCONF = 'Chatter.urls'

# Templates configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Specify any custom directories if needed
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

# ASGI application (since you're using Daphne/Channels)
ASGI_APPLICATION = "Chatter.asgi.application"

# Database configuration using dj_database_url for easier parsing
DATABASES = {
    'default': dj_database_url.parse(
        "postgresql://chatter_data_ekw1_user:qrLew41Zbb7VuLsv3h6IFxHLes1h7rcA@dpg-crpe49tds78s73d8qrcg-a.singapore-postgres.render.com/chatter_data_ekw1"
    )
}

# Password validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Localization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static and media files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'

# Email backend configuration (for sending emails)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'otpkjaef@gmail.com'
EMAIL_HOST_PASSWORD = 'djkbolzvzmcyambl'

# Custom user model
AUTH_USER_MODEL = 'core.User'

# Django Rest Framework settings with JWT authentication
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# Simple JWT configuration
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

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# Channel Layers configuration for WebSocket with Redis
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [
                f"redis://:{'TBQWaozZBxxHWiLFmuG1tmf6YySHMb5I'}@redis-15562.c305.ap-south-1-1.ec2.redns.redis-cloud.com:15562"
            ],
        },
    },
}

# Logging configuration
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

# Cloudinary storage configuration for static and media files
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dtfo1nvhr',
    'API_KEY': '921286418385759',
    'API_SECRET': 'TXTSpg5xl0m3RbkvLWvHg4frFLw',
}

# Static files storage with Cloudinary
STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticHashedCloudinaryStorage'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.RawMediaCloudinaryStorage'
