# -*- coding: utf-8 -*-
""" 
@author: xingxingzaixian
@create: 2020/9/6
@description: 
"""
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class UserInfo(AbstractUser):
    nickname = models.CharField(max_length=32, help_text='昵称')
    telephone = models.CharField(max_length=11, blank=True, null=True, unique=True, help_text='手机号码')
    create_time = models.DateTimeField(auto_now_add=True, help_text='创建时间')

    class Meta:
        db_table = 'tbl_user'
