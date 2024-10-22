from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-v6o(p*%9@a=q$w^###@7kbc32mi=44e-hw2w6v=)o&gn2_1v+8"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8001",  # 添加开发服务器地址
    "http://127.0.0.1:8001",
    # 'https://your-domain.com',  # 生产环境时添加的域名
]

# Application definition

INSTALLED_APPS = [
    "jazzmin",  # Django admin theme
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third-party apps
    "corsheaders",
    "ninja_extra",
    "ninja_jwt",
    # local apps
    "cpc",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # 添加 CORS 中间件
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CORS_URLS_REGEX = r"^/api/.*$"
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # next.js
    "http://127.0.0.1:3000",
]

ROOT_URLCONF = "graceful_backend.urls"

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

WSGI_APPLICATION = "graceful_backend.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "gracefulmanager",
        "USER": "postgres",
        "PASSWORD": "graceful@pg2024",
        "HOST": "160.16.234.163",
        "PORT": "5432",  # PostgreSQL 默认端口
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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

# LANGUAGE_CODE = "en-us"
LANGUAGE_CODE = "zh-hans"

# TIME_ZONE = "UTC"
TIME_ZONE = "Asia/Tokyo"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# scrapyd 配置
# SCRAPYD_URL = "http://localhost:6800"
SCRAPYD_URL = "http://scrapyd:6800"  # 因为使用了 Docker Compose，所以这里使用服务名
# SCRAPYD_URL = os.getenv("SCRAPYD_URL", "http://localhost:6800")  # 从环境变量中获取 Scrapyd 的地址


# Celery 配置
CELERY_BROKER_URL = "redis://redis:6379/0"  # Redis 作为 Broker
CELERY_RESULT_BACKEND = "redis://redis:6379/1"  # 使用 Redis 存储任务结果

CELERY_ACCEPT_CONTENT = ["json"]  # 指定接受的内容类型
CELERY_TASK_SERIALIZER = "json"  # 指定任务序列化方式
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "Asia/Tokyo"  # 根据需要设置你的时区


INSTALLED_APPS += [
    "django_celery_beat",
    "django_celery_results",
]

# 将 Celery 的结果存储在 Django ORM 中
CELERY_RESULT_BACKEND = "django-db"
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers.DatabaseScheduler"


NINJA_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}
