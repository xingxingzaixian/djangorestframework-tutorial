# -*- coding: utf-8 -*-
""" 
@author: xingxingzaixian
@create: 2020/9/6
@description: 
"""
from django.db.models import Q
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.generics import GenericAPIView
from drf_spectacular.utils import extend_schema

from users.models import UserInfo
from users.serializers import LoginSerivalizer, RegisterSerivalizer
from utils.logger import getLogger
from utils.constant import RESPONSE_SUCCESS, RESPONSE_FAILURE
from utils.response import AuthenticationFailedSerializer

logger = getLogger('request')
# Create your views here.
class LoginView(GenericAPIView):
    authentication_classes = []
    # 这里的 serializer_class 将会提供给 API 文档生成
    serializer_class = LoginSerivalizer

    @extend_schema(
        responses={200: str, 403: AuthenticationFailedSerializer},
        summary='登录'
    )
    def post(self, request: Request):
        ser = LoginSerivalizer(data=request.data)
        ser.is_valid(raise_exception=True)

        username = ser.data.get('username')
        password = ser.data.get('password')

        try:
            user = authenticate(request, username=username, password=password)
            return Response(user.token)
        except (UserInfo.DoesNotExist, UserInfo.MultipleObjectsReturned) as e:
            return Response()


class RegisterView(GenericAPIView):
    authentication_classes = []
    serializer_class = RegisterSerivalizer

    @extend_schema(
        responses={200: str, 400: None},
        summary='注册'
    )
    def post(self, request: Request):
        ser = RegisterSerivalizer(data=request.data)
        ser.is_valid(raise_exception=True)

        username = ser.data.get('username')
        password = ser.data.get('password')
        nickname = ser.data.get('nickname')
        telephone = ser.data.get('telephone')

        try:
            UserInfo.objects.get(Q(username=username) | Q(telephone=telephone))
        except (UserInfo.DoesNotExist, UserInfo.MultipleObjectsReturned) as e:
            user = UserInfo(username=username)
            user.set_password(password)
            user.nickname = nickname
            user.telephone = telephone
            # 我们无需额外激活账号，所以注册是自动激活
            user.is_active = True
            user.save()
            logger.info(f'用户: {username} 注册成功')
            return Response(RESPONSE_SUCCESS)
        else:
            return Response(RESPONSE_FAILURE)
