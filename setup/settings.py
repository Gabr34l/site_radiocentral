"""
setup/settings.py — Configurações centrais do projeto Django.

Este arquivo controla TUDO no projeto: banco de dados, segurança,
arquivos estáticos, internacionalização, apps instalados, etc.

Variáveis sensíveis (SECRET_KEY, DATABASE_URL, DEBUG) são lidas
do arquivo .env via python-dotenv, para não ficarem expostas no código.

Ambientes suportados:
  - Desenvolvimento local: DEBUG=True, SQLite, arquivos servidos pelo Django
  - Produção (PythonAnywhere): DEBUG=False, PostgreSQL/MySQL via DATABASE_URL,
    arquivos estáticos servidos pelo servidor web (WhiteNoise para estáticos)
"""
from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# Configurações de Segurança
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-default-key-change-me')
DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'gabr34l.pythonanywhere.com,localhost,127.0.0.1').split(',')

# Definição de Aplicativos
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'centralfm',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'setup.urls'

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

WSGI_APPLICATION = 'setup.wsgi.application'

# Banco de Dados
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
        conn_max_age=600
    )
}

# Internacionalização
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# Arquivos Estáticos e de Mídia
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Configuração do Jazzmin (Admin Premium)
JAZZMIN_SETTINGS = {
    "site_title": "Administração Central FM",
    "site_header": "Central FM 101.1",
    "site_brand": "Central FM",
    "site_logo": "Logo/logo.png",
    "welcome_sign": "Bem-vindo ao Painel da Central FM",
    "copyright": "Rádio Central — 101.1 FM",
    "show_sidebar": True,
    "navigation_expanded": True,
    "order_with_respect_to": ["centralfm", "auth"],
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "centralfm.Locutor": "fas fa-microphone-alt",
        "centralfm.Programa": "fas fa-calendar-alt",
        "centralfm.Promocao": "fas fa-gift",
        "centralfm.Ganhador": "fas fa-trophy",
    },
    "site_logo_classes": "img-circle",
    "changeform_format": "horizontal_tabs",
    "show_ui_builder": False,
    "custom_css": "admin/css/custom_admin.css",
}

JAZZMIN_UI_SETTINGS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-success",
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_fixed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-success",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "flatly",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-success",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}

# Validação de Senhas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
