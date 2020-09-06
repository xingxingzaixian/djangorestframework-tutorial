# -*- coding: utf-8 -*-
""" 
@author: xingxingzaixian
@create: 2020/9/6
@description: 
"""
import logging
from django.db.models import Q
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import UserInfo
from users.serializers import LoginSerivalizer, RegisterSerivalizer

LOG = logging.getLogger('request')


# Create your views here.
class LoginView(APIView):
    authentication_classes = []

    def post(self, request):
        ser = LoginSerivalizer(data=request.data)
        ser.is_valid(raise_exception=True)

        username = ser.data.get('username')
        password = ser.data.get('password')

        ret = {'result': 'success', 'detail': ''}
        try:
            user = authenticate(request, username=username, password=password)
            ret['detail'] = '登录成功'
            ret['token'] = user.token
        except (UserInfo.DoesNotExist, UserInfo.MultipleObjectsReturned) as e:
            ret['detail'] = '用户名或密码错误'

        return Response(ret)


class RegisterView(APIView):
    authentication_classes = []

    def post(self, request):
        ser = RegisterSerivalizer(data=request.data)
        ser.is_valid(raise_exception=True)

        username = ser.data.get('username')
        password = ser.data.get('password')
        ret = {'result': 'failure', 'detail': ''}

        try:
            UserInfo.objects.get(Q(username=username) | Q(telephone=username))
        except (UserInfo.DoesNotExist, UserInfo.MultipleObjectsReturned) as e:
            user = UserInfo(username=username)
            user.set_password(password)

            # 我们无需额外激活账号，所以注册是自动激活
            user.is_active = True
            user.save()
            ret['result'] = 'success'
            ret['detail'] = '注册成功'
            LOG.info('用户: %s 注册成功', username)
        else:
            ret['detail'] = '用户已注册'

        return Response(ret)
