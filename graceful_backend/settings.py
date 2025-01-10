from datetime import timedelta
import os
from pathlib import Path
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# 初始化 environ
env = environ.Env()

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

print("env:=========", env("DB_NAME"))

SECRET_KEY = env("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8001",  # 添加开发服务器地址
    "http://127.0.0.1:8001",
    "http://160.16.234.163:8035",
    "https://160.16.234.163:8035",
    "https://160.16.234.163:3000",
    "http://160.16.234.163:3000",
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
    "shares",
    "cpc",
    "reports",
    "data_management",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # 添加 CORS 中间件
    "django.middleware.common.CommonMiddleware",
    #
    # "django.middleware.gzip.GZipMiddleware",
    # "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
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


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    }
}


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


# LANGUAGE_CODE = "en-us"
LANGUAGE_CODE = "zh-hans"

# TIME_ZONE = "UTC"
TIME_ZONE = "Asia/Tokyo"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "statics/"

# # 静态文件存放的目录
STATIC_ROOT = os.path.join(BASE_DIR, "statics")

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# scrapyd 配置

# SCRAPYD_URL = "http://localhost:6800"
SCRAPYD_URL = env("SCRAPYD_URL")
print("SCRAPYD_URL: ", SCRAPYD_URL)
# ===============================================

# worker每次取任务的数量
CELERYD_PREFETCH_MULTIPLIER = 1
# 防止死锁
CELERYD_FORCE = True
# CELERY与RabbitMQ增加60秒心跳设置项
BROKER_HEARTBEAT = 60

# Celery 配置
CELERY_BROKER_URL = env("BROKER_URL")
# CELERY_BROKER_URL = env("CELERY_BROKER_URL")  # Redis 作为 Broker
# CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND")  # 使用 Redis 存储任务结果

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

# ===============================================

NINJA_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
}


PAGE_SIZE = 30
