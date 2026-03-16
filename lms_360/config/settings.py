from pathlib import Path
import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-dljzh-x)7s#xd2r&3ntv37ju-n0!=rxs_vco1!=qsbj9vz99gx'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'drf_spectacular',
    'drf_spectacular_sidecar',

    # Custom apps
    'users',
    'courses',
    'dashboard',
    'assignments',
    'discussions',
    'schedule',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
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
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'users.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SIMPL_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes = 60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days = 7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'LMS_360 API',
    'DESCRIPTION': '''
    LMS_360 is a comprehensive Learning Management System API that provides:

    ## Features
    - **User Management**: Registration, authentication, and profile management
    - **Course Management**: Browse, enroll, and manage courses
    - **Content Delivery**: Lessons, assignments, and progress tracking
    - **Discussion Forums**: Community interaction and Q&A
    - **Live Sessions**: Scheduled virtual classes
    - **Dashboard**: Learning analytics and task management

    ## Authentication
    All endpoints except registration and login require JWT authentication.
    Include the token in the Authorization header: `Bearer <token>`

    ## User Roles
    - **Student**: Can enroll in courses, view content, submit assignments
    - **Instructor**: Can create and manage courses, grade assignments
    - **Admin**: Full system access

    ## Common Response Codes
    - 200: Success
    - 201: Created
    - 400: Bad Request
    - 401: Unauthorized
    - 403: Forbidden
    - 404: Not Found
    ''',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    # Use sidecar for UI assets
    'SWAGGER_UI_DIST': 'SIDECAR',
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'TAGS': [
        {'name': 'Authentication', 'description': 'User registration and login'},
        {'name': 'User Profile', 'description': 'User profile management'},
        {'name': 'Courses', 'description': 'Course browsing and enrollment'},
        {'name': 'Lessons', 'description': 'Lesson content and progress'},
        {'name': 'Assignments', 'description': 'Assignment submission and grading'},
        {'name': 'Discussions', 'description': 'Discussion forums and replies'},
        {'name': 'Dashboard', 'description': 'Learning analytics and todos'},
        {'name': 'Schedule', 'description': 'Live lesson scheduling'},
    ],
}


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
