# -*- coding: utf-8 -*-
""" 
@author: xingxingzaixian
@create: 2020/9/6
@description: 
"""
import time
from jwt import JWT, jwk_from_dict
from django.conf import settings


class JwtUtil:
    def __init__(self):
        self.verifying_key = jwk_from_dict({
            'kty': 'oct',
            'kid': 'HMAC key used in JWS A.1 example',
            'k': settings.SECRET_KEY
        })

    def gen_jwt_token(self, user):
        token_dict = {
            'username': user.username,
            'phone': user.telephone,
            'exp': time.time() + 24 * 3600,
            'iat': time.time()
        }

        obj = JWT()
        token = obj.encode(token_dict, key=self.verifying_key)
        return token

    def check_jwt_token(self, value):
        obj = JWT()
        data = None
        try:
            data = obj.decode(value, key=self.verifying_key)
        except Exception as e:
            print(e)

        return data
