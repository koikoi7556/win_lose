import environ
from .base import *


# Read .env if exists
env = environ.Env()
env.read_env(os.path.join(BASE_DIR))


# Security settins
DEBUG = False
SECRET_KEY = env('SECRET_KEY')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')


# Database
# よくわからんがリンクを見て。。HerokuとかPythonanywhere使うときはいらないと思われる。
# DATABASES = {
#     'default': env.db()
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'win_lose',
        'USER': 'name',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}


# ビューから例外が漏れてしまった場合にビュー何でのデータベースの保存更新削除がすべてロールバックされる。
DATABASES['default']['ATOMIC_REQUESTS'] = True
# Logging
LOGGING = {
    # バージョンは「1」固定
    'version': 1,
    # 既存のログ設定を無効化しない
    'disable_existing_loggers': False,
    # ログフォーマット
    'formatters': {
        # 本番用
        'production': {
            'format': '%(asctime)s [%(levelname)s] %(process)d %(thread)d '
                      '%(pathname)s:%(lineno)d %(message)s'
        },
    },
    # ハンドラ
    'handlers': {
        # ファイル出力用ハンドラ
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/{}/app.log'.format(PROJECT_NAME),
            'formatter': 'production',
        },
    },
    # ロガー
    'loggers': {
        # 自作アプリケーション全般のログを拾うロガー
        '': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
        # Django本体が出すログ全般を拾うロガー
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}


# データベースの接続情報を環境変数から指定できるようにする（変数名は「DATABASE_URL」）。無料のHerokuデータベースを特に設定せずに使えるのはこの仕組みを利用しているから。

import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)