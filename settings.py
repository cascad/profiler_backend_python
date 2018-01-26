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

DEBUG = env.bool('DEBUG')

HOST = env.str('HOST')
PORT = env.int('PORT')
MONGO_HOST = env.str('MONGO_HOST')
MONGO_DB_NAME = env.str('MONGO_DB_NAME')
STATIC_PATH = env.str('STATIC_PATH')
TEMPLATE_PATH = env.str('TEMPLATE_PATH')
PROCESSOR_INTERVAL = env.int('PROCESSOR_INTERVAL')
DATASET_COLLECTION = 'ldoe'
