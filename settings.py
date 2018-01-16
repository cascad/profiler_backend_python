from os.path import isfile

import os
from envparse import env
import logging

log = logging.getLogger('app')
log.setLevel(logging.DEBUG)

f = logging.Formatter('[L:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(f)
log.addHandler(ch)

if isfile('environments.env'):
    env.read_envfile('environments.env')

DEBUG = env.bool('DEBUG', default=True)

SITE_HOST = env.str('HOST', default="192.168.2.209")
SITE_PORT = env.int('PORT', default=8002)
SECRET_KEY = env.str('SECRET_KEY', default='Thirty  two  length  bytes  key.')
MONGO_HOST = env.str('MONGO_HOST', default='192.168.99.100:27017')
MONGO_DB_NAME = env.str('MONGO_DB_NAME', default='performance_logs')
STATIC_PATH = env.str('STATIC_PATH', default=os.getcwd() + "/web_anal_static")
TEMPLATE_PATH = env.str('TEMPLATE_PATH', default='web_anal_static')
PROCESSOR_INTERVAL = env.int('PROCESSOR_INTERVAL', default=120)
DATASET_COLLECTION = 'ldoe'
