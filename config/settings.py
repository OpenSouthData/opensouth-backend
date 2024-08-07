"""
Django settings for config project.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path
from django.utils.timezone import timedelta

from configurations import Configuration, values
# import firebase_admin
# from firebase_admin import credentials
import json
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())



    
# FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS")

# cred = credentials.Certificate(json.loads(FIREBASE_CREDENTIALS))
# firebase_admin.initialize_app(cred)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS").split(',')
CSRF_TRUSTED_ORIGINS = os.getenv("TRUSTED_ORIGINS").split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',

    'django_extensions',
    'debug_toolbar',

    'accounts.apps.AccountsConfig',
    'main.apps.MainConfig',
    'admins.apps.AdminConfig',
    'public.apps.PublicConfig',
    'api_portal.apps.ApiPortalConfig',
    "social_auth",
    
    'rest_framework',
    'django_filters',
    'djoser',
    'drf_yasg',
    'coreapi',
    'corsheaders',
    'rest_framework_simplejwt.token_blacklist',
    'storages',

]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # 'config.translate.TranslationMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

APPEND_SLASH=True


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Lagos'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# ##AWS S3 settings

AWS_ACCESS_KEY_ID = os.getenv("AWS_Access_Key")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_Secret_Access_Key")
AWS_S3_REGION_NAME = os.getenv("AWS_Storage_Region")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_Storage_Bucket_Name")
# AWS_S3_CUSTOM_DOMAIN = "d1cc9gva10xzzu.cloudfront.net"
# AWS_CLOUDFRONT_KEY_ID = os.getenv("AWS_Cloudfront_Key_ID")
# AWS_CLOUDFRONT_KEY = str(os.getenv("AWS_Cloudfront_Private_Key").encode('utf-8').strip())
# print(AWS_CLOUDFRONT_KEY)

# AWS_QUERYSTRING_EXPIRE = 180


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.User'



DJOSER = {
    "USER_ID_FIELD" : "id",
    'LOGIN_FIELD': 'email',
    'USER_CREATE_PASSWORD_RETYPE': True,
    'USERNAME_CHANGED_EMAIL_CONFIRMATION':True,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION':True,
    'SEND_ACTIVATION_EMAIL':False,
    'SEND_CONFIRMATION_EMAIL':False,
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': 'username/reset/confirm/{uid}/{token}',
    "PASSWORD_RESET_CONFIRM_RETYPE" : True,
    "SET_PASSWORD_RETYPE" : True,
    "PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND":True,
    'ACTIVATION_URL' : 'activate/{uid}/{token}',
    'SERIALIZERS':{
        'user_create': 'accounts.serializers.UserRegistrationSerializer',
        'user': 'accounts.serializers.CustomUserSerializer',
        'user_delete': 'accounts.serializers.UserDeleteSerializer',
        "current_user" : 'accounts.serializers.CustomUserSerializer',
    },
    "EMAIL" : {
        'password_reset': 'accounts.emails.CustomPasswordResetEmail',  
    } 
}


REST_FRAMEWORK = {

    # 'DEFAULT_AUTHENTICATION_CLASSES': (
    #     'rest_framework_simplejwt.authentication.JWTAuthentication',
    # ),

    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer'
    ],

    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FormParser',
    ),


    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    # "PAGE_SIZE": 10,
    
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=3),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=5),
    'UPDATE_LAST_LOGIN': True,
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    

}

#Cors headers
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True


SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_PRELOAD = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = 31536000
SECURE_REDIRECT_EXEMPT = []
SECURE_SSL_HOST = None
SECURE_SSL_REDIRECT = False
SECURE_PROXY_SSL_HEADER = (
    ('HTTP_X_FORWARDED_PROTO', 'https')
)

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
        }
    }


AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.AllowAllUsersModelBackend']


LOGIN_URL = '/admin/login/'
SITE_NAME = ""
DOMAIN = ""

#OAuth credentials
GOOGLE_CLIENT_ID= os.getenv("GOOGLE_CLIENT_ID")



# Configure the logging settings
LOG_DIR = os.path.join(BASE_DIR, 'logs')

# Ensure the logs directory exists
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Logging configuration for errors
LOG_FILE_ERROR = os.path.join(LOG_DIR, 'error.log')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': LOG_FILE_ERROR,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['error_file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# Logging configuration for server prints
LOG_FILE_SERVER = os.path.join(LOG_DIR, 'server.log')
LOGGING['handlers']['server_file'] = {
    'level': 'INFO',
    'class': 'logging.FileHandler',
    'filename': LOG_FILE_SERVER,
    'formatter': 'verbose',
}
LOGGING['loggers']['django.server'] = {
    'handlers': ['server_file'],
    'level': 'INFO',
    'propagate': False,
}

# Logging formatter
LOGGING['formatters'] = {
    'verbose': {
        'format': '%(asctime)s [%(levelname)s] %(message)s',
        'datefmt': '%Y-%m-%d %H:%M:%S',
    },
}



if os.getenv("ENVIRONMENT") == "production":

    """
    The in-production settings.
    """
    DEBUG = True

    INTERNAL_IPS = [
        '127.0.0.1'
    ]
    
    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv("prod_db_name"),
            'HOST': os.getenv("prod_db_host"),
            'USER': os.getenv("prod_db_user"),
            'PASSWORD': os.getenv("prod_db_password"),
            'PORT': os.getenv("prod_db_port")

        }
    }






if os.getenv("ENVIRONMENT") == "development":
    """
    The in-development settings and the default configuration.
    """
    DEBUG = True

    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv("db_name"),
            'HOST': os.getenv("db_host"),
            'USER': os.getenv("db_user"),
            'PASSWORD': os.getenv("db_password"),
            'PORT': os.getenv("db_port")

        }
    }





if os.getenv("ENVIRONMENT") == "local":
    
    DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3'
            }
        }

