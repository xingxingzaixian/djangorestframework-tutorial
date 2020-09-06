# -*- coding: utf-8 -*-
""" 
@author: xingxingzaixian
@create: 2020/9/6
@description: 
"""
from django.contrib.auth import backends
from django.db.models import Q
from users.models import UserInfo
from utils.jwt_util import JwtUtil


class UserBackend(backends.ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = UserInfo.objects.get(Q(username=username) | Q(telephone=username))
        if user.check_password(password):
            jwt = JwtUtil()
            token = jwt.gen_jwt_token(user)
            user.token = token
            return user
        raise UserInfo.DoesNotExist(
            "UserInfo matching query does not exist."
        )
