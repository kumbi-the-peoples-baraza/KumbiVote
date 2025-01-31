"""
Django settings for kumbivote project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from datetime import timedelta
from pathlib import Path

import psycopg2.extensions
from decouple import config

# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third Party
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework.authtoken",
    "corsheaders",
    "oauth2_provider",
    # Internal
    "apps.elections",
    "apps.organizations",
    "apps.users",
    "apps.common",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

AUTH_USER_MODEL = "users.User"

ROOT_URLCONF = "core.urls"

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "oauth2_provider.backends.OAuth2Backend",
)

GOOGLE_API_KEY = ""
GOOGLE_API_SECRET = ""

OAUTH2_PROVIDER = {
    "ACCESS_TOKEN_EXPIRE_SECONDS": 3600,  # Token expiration time in seconds
    "AUTHORIZATION_CODE_EXPIRE_SECONDS": 3600,
    "REFRESH_TOKEN_EXPIRE_SECONDS": 86400,
    "SCOPES": {"read": "Read Scope", "write": "Write Scope"},
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost",
]

CORS_ALLOW_ALL_ORIGINS = True
ASGI_APPLICATION = "core.asgi.application"

# PKI Configuration
KV_SECRETS_PATH = config("SECRETS_PATH")
PKI_PRIVATE = KV_SECRETS_PATH + config("PKI_PRIV_DEV")
PKI_PUBLIC = KV_SECRETS_PATH + config("PKI_PUB_DEV")

with open(os.path.join(BASE_DIR, PKI_PRIVATE)) as f:
    KV_PRIVATE_KEY = f.read()

with open(os.path.join(BASE_DIR, PKI_PUBLIC)) as f:
    KV_PUBLIC_KEY = f.read()

# JWT Configuration
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}

SIMPLE_JWT = {
    "ALGORITHM": "RS256",
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "SIGNING_KEY": KV_PRIVATE_KEY,
    "VERIFYING_KEY": KV_PUBLIC_KEY,
    "ISSUER": "KumbiVote",
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "AUTH_COOKIE": "AccessToken",
    "AUTH_COOKIE_REFRESH": "RefreshToken",
    "AUTH_COOKIE_HTTPONLY": True,
    "AUTH_COOKIE_SAMESITE": "Lax",
    "AUTH_COOKIE_SECURE": False,
    "USER_ID_FIELD": "uuid",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASS"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT"),
        "OPTIONS": {
            "client_encoding": "UTF-8",
            "isolation_level": psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE,
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{asctime} {levelname} {module} {message}",
            "style": "{",
        },
        "database": {
            "format": """{asctime} {levelname} {module} {message} {sql} {params} {alias} {duration}""",
            "style": "{",
        },
        "simple": {
            "simple": {
                "format": "{asctime} {levelname} {message}",
                "style": "{",
            },
        },
        "filters": {
            "require_debug_false": {
                "()": "django.utils.log.RequireDebugFalse",
            },
        },
        "handlers": {
            # Output log messages to console
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            },
            # Save logs to a file
            "file": {
                "level": "INFO",
                "class": "logging.FileHandler",
                "filename": os.path.join(BASE_DIR, "logs/global.log"),
                "formatter": "verbose",
            },
            "security": {
                "level": "INFO",
                "class": "logging.FileHandler",
                "filename": os.path.join(BASE_DIR, "logs/security.log"),
                "formatter": "verbose",
            },
            # Log websocket events
            "websocket": {
                "level": "INFO",
                "class": "logging.FileHandler",
                "filename": os.path.join(BASE_DIR, "logs/websocket.log"),
                "formatter": "verbose",
            },
            # Log HTTP requests
            "requests": {
                "level": "INFO",
                "class": "logging.FileHandler",
                "filename": os.path.join(BASE_DIR, "logs/requests.log"),
                "formatter": "verbose",
            },
            # Log database queries
            "database": {
                "level": "DEBUG",
                "class": "logging.FileHandler",
                "filename": os.path.join(BASE_DIR, "logs/database.log"),
                "formatter": "database",
            },
            # Log admin actions
            "admin": {
                "level": "DEBUG",
                "class": "logging.FileHandler",
                "filename": os.path.join(BASE_DIR, "logs/admin.log"),
                "formatter": "verbose",
            },
            "auth": {
                "level": "ERROR",
                "class": "logging.FileHandler",
                "filename": os.path.join(BASE_DIR, "logs/auth.log"),
                "formatter": "verbose",
            },
        },
        "loggers": {
            # Default logger for the Django project
            "django": {
                "handlers": ["console", "file"],
                "level": "DEBUG",  # You can switch to 'INFO' in production
                "propagate": True,
            },
            # Logs for security-related events, such as logins
            "django.security": {
                "handlers": ["security"],
                "level": "INFO",
                "propagate": True,
            },
            # log errors
            "django.error": {
                "handlers": ["error"],
                "level": "ERROR",
                "propagate": True,
            },
            # Logs websocket events
            "websocket": {
                "handlers": ["websocket"],
                "level": "INFO",
                "propagate": False,
            },
            # Logs requests
            "django.request": {
                "handlers": ["requests"],
                "level": "INFO",
                "propagate": True,
            },
            # Log database queries (use with caution; can generate huge logs)
            "django.db.backends": {
                "level": "DEBUG",  # Set to 'DEBUG' to log all queries
                "handlers": ["database"],
                "propagate": True,
            },
            # Your custom application logger
            "django.admin": {
                "handlers": ["admin"],
                "level": "DEBUG",
                "propagate": True,
            },
            "django.contrib.auth": {
                "handlers": ["auth"],
                "level": "ERROR",
                "propagate": True,
            },
        },
    },
}
# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

USE_TZ = True

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Nairobi"

USE_I18N = True

# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# X_FRAME_OPTIONS = "DENY"
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
