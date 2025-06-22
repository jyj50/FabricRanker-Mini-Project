"""
Django settings.py에 추가해야 할 설정들
"""

import os
from pathlib import Path

# 기본 설정 (이미 있다면 수정)
BASE_DIR = Path(__file__).resolve().parent.parent

# 미디어 파일 설정
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# 앱 등록
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "fabric_prediction",  # 새로 추가
]

# 정적 파일 설정
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# 파일 업로드 설정
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB

# 로깅 설정
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "fabric_prediction.log",
        },
    },
    "loggers": {
        "fabric_prediction": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

# 이미지 처리를 위한 Pillow 설정
# pip install Pillow 필요
