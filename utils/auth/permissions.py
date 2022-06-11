import os

import casbin
from casbin_adapter.adapter import Adapter
from rest_framework.permissions import BasePermission
from django.conf import settings


class IsSuperUser(BasePermission):
    """
    超级用户默认拥有所有权限
    """
    def has_permission(self, request, view):
        return bool(request.user.is_superuser)


class CasbinAdapter:
    adapter = Adapter()
    model = os.path.join(settings.BASE_DIR, 'config/model.conf')
    enforce = casbin.Enforcer(model, adapter, True)
    
    @classmethod
    def add_role_permission(cls, role, data, permission):
        '''
        添加角色对数据处理的权限
        '''
        cls.enforce.add_policy(role, data, permission)
        
    @classmethod
    def remove_role_permission(cls, role, data, permission):
        '''
        删除角色对数据处理的权限
        '''
        cls.enforce.remove_policy(role, data, permission)
        
    @classmethod
    def add_user_permission(cls, username, data, permission):
        '''
        添加用户对数据处理的权限
        '''
        cls.enforce.add_permission_for_user(username, data, permission)
        
    @classmethod
    def remove_permission_for_user(cls, username, data, permission):
        '''
        删除用户对数据处理的权限
        '''
        cls.enforce.delete_permission_for_user(username, data, permission)
    
    @classmethod
    def remove_permissions_for_user(cls, username):
        '''
        删除用户的所有权限
        '''
        cls.enforce.delete_permissions_for_user(username)
    
    @classmethod
    def get_permissions_for_user(cls, username, inherit=None):
        '''
        查询用户所有权限
        inherit:
            True: 获取用户所有权限，包括角色继承的权限
            False/None: 只获取用户直接权限，不包含角色携带的权限
        '''
        if inherit:
            cls.enforce.get_implicit_permissions_for_user(username)
        return cls.enforce.get_permissions_for_user(username)
        
    @classmethod
    def add_role_for_user(cls, username, role):
        '''
        添加用户角色
        '''
        cls.enforce.add_role_for_user(username, role)
        
    @classmethod
    def add_role_for_role(cls, role1, role2):
        '''
        为角色添加角色，即role1继承role2的所有权限
        '''
        cls.enforce.add_role_for_user(role1, role2)
        
    @classmethod
    def remove_role_for_user(cls, username, role):
        '''
        删除用户角色
        '''
        cls.enforce.delete_role_for_user(username, role)
        
    @classmethod
    def remove_roles_for_user(cls, username):
        '''
        删除用户所有角色
        '''
        cls.enforce.delete_roles_for_user(username)
        
    @classmethod
    def get_roles_for_user(cls, username, inherit=None):
        '''
        获取用户所有角色
        inherit:
            True: 获取用户所有权限，包括角色继承的权限
            False/None: 只获取用户直接权限，不包含角色携带的权限
        '''
        if inherit:
            return cls.enforce.get_implicit_roles_for_user(username)
        return cls.enforce.get_roles_for_user(username)
        
    @classmethod
    def remove_user(cls, username):
        '''
        删除用户及相关权限和角色记录
        '''
        cls.enforce.delete_user(username)
        
    @classmethod
    def remove_role(cls, role):
        '''
        删除角色及相关用户、权限记录
        '''
        cls.enforce.delete_role(role)
        
    @classmethod
    def remove_permission(cls, permission):
        '''
        删除权限及相关用户、角色记录
        '''
        cls.enforce.delete_permission(permission)
    