# -*- coding: utf-8 -*-
""" 
@author: xingxingzaixian
@create: 2020/8/24
@description: 
"""
from settings.settings import *

DEBUG = False

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db_pro.sqlite3'),
    }
}
