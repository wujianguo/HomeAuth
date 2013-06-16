#! /usr/bin/env python
# -*- coding: utf-8 -*-
# settings for homeauth project.

import os
ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
LOG_DIR = os.path.join(ROOT_DIR,'log')
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)
CODE_DIR = os.path.join(ROOT_DIR,'downcode')
if not os.path.exists(CODE_DIR):
    os.mkdir(CODE_DIR)
SCREEN_DIR = os.path.join(ROOT_DIR,'screen')
if not os.path.exists(SCREEN_DIR):
    os.mkdir(SCREEN_DIR)
CAMERA_DIR = os.path.join(ROOT_DIR,'camera')
if not os.path.exists(CAMERA_DIR):
    os.mkdir(CAMERA_DIR)
#proxy
PROXY = None
#PROXY = {'http':'http://127.0.0.1:9341'}
PROXY_USER = ''
PROXY_PAWD = ''

#serveurls
ID_RSA_PUB = 'http://ha.wujianguo.org/static/key/id_rsa.pub'
GET_CMD_URL = 'http://ha.wujianguo.org/recvcmd'
UPDATE_INFO_URL = 'http://ha.wujianguo.org/updateinfo'

#ID_RSA_PUB = 'http://localhost:8080/static/key/id_rsa.pub'
#GET_CMD_URL = 'http://localhost:8080/recvcmd'


EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''

#recv msg for comfirm dropbox
RECV_MSG_EMAIL = ''

#dropbox info
APP_KEY=''
APP_SECRET=''
ACCESS_TYPE=''

USER_EMAIL = 'lsjustin89@gmail.com'
USER_PRIVKEY_PATH = os.path.join(ROOT_DIR,'id_rsa')
import datetime
REQUESTS_TIME = datetime.timedelta(seconds=5)
TIME_OUT = 20
# Logging
LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '[%(levelname)s %(asctime)s %(filename)s %(module)s %(funcName)s %(lineno)d] %(message)s'
        },
        'simple': {
            'format': '[%(levelname)s %(module)s %(lineno)s] %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'log_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(LOG_DIR,'homeauth.log'),
            'maxBytes': 1024*1024*20, # 20 MB
            'backupCount': 5,
        },
    },
    'loggers': {
        'cmd': {
            'handlers': ['console', 'log_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'audio': {
            'handlers': ['console', 'log_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'screen': {
            'handlers': ['console', 'log_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'camera': {
            'handlers': ['console', 'log_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        # Catch All Logger -- Captures any other logging
        '': {
            'handlers': ['console', 'log_file'],
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}
import logging.config
logging.config.dictConfig(LOGGING)
