# 更新记录
### 2022-06-06
- 更新项目依赖为最新
- 使用logru作为日志记录模块
- 删除 API 文档 coreapi，修改为 drf_spectacular

### 2021-07-23
- 重新使用 Django 3.2.4 构建项目
- 增加 API 文档库 coreapi


## 需要安装的Python库

- django
- djangorestframework
- django-cors-headers
- python-jose
- drf_spectacular
- drf_spectacular_sidecar
- pymysql
- django-filter
- loguru

## 初始化Django工程

```shell
django-admin startproject backend
```

创建好工程后，我们要对目录和配置进行一些调整，首先在根目录下创建两个目录：apps和utils，将所有的app都存放到apps目录里面，utils目录下存放通用处理函数，这样我们的根目录就更加清晰了

![](https://s3.bmp.ovh/imgs/2022/06/06/f7f44ab816b75c5f.jpg)

## 增加多数据库配置

- 在backend目录下增加router.py文件

  路由配置文件当中的返回值是我们在DATABASES中配置的键，默认是default，按照一定的条件返回不同的键，每个键内配置不同的数据库连接，就可以实现Django项目连接多个数据库

  ```python
  class CustomRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label in settings.DATABASE_APPS_MAPPING:
            return settings.DATABASE_APPS_MAPPING[model._meta.app_label]

    def db_for_write(self, model, **hints):
        if model._meta.app_label in settings.DATABASE_APPS_MAPPING:
            return settings.DATABASE_APPS_MAPPING[model._meta.app_label]

    def allow_relation(self, obj1, obj2, **hints):
        db_obj1 = settings.DATABASE_APPS_MAPPING.get(obj1._meta.app_label)
        db_obj2 = settings.DATABASE_APPS_MAPPING.get(obj2._meta.app_label)
        if db_obj1 and db_obj2:
            if db_obj1 == db_obj2:
                return True
            else:
                return False

    def allow_syncdb(self, db, model):
        if db in settings.DATABASE_APPS_MAPPING.values():
            return settings.DATABASE_APPS_MAPPING.get(model._meta.app_label) == db
        elif model._meta.app_label in settings.DATABASE_APPS_MAPPING:
            return False

    def allow_migrate(self, db, app_label, model=None, **hints):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        if db in settings.DATABASE_APPS_MAPPING.values():
            return settings.DATABASE_APPS_MAPPING.get(app_label) == db
        elif app_label in settings.DATABASE_APPS_MAPPING:
            return False
        return None
  ```

- 在settings.py文件中增加路由配置

  ```python
  DATABASE_ROUTERS = ['backend.router.CustomRouter']
  ```

## 设置自定义用户模型

- 在apps下增加users应用

  在models.py下增加如下内容

  ```python
  from django.contrib.auth.models import AbstractUser
  from django.db import models
  from uuid import uuid4
  
  
  # Create your models here.
  
  class UserInfo(AbstractUser):
      uid = models.CharField(max_length=36, default=uuid4, primary_key=True)
      nickname = models.CharField(max_length=32, verbose_name='昵称')
      telephone = models.CharField(max_length=11, blank=True, null=True, unique=True, verbose_name='手机号码')
      create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
  
      class Meta:
          db_table = 'tbl_user'
  ```

- 在settings.py中增加如下内容

  ```python
  INSTALLED_APPS = [
    ...
    'users'
  ]
  
  AUTH_USER_MODEL = 'users.UserInfo'
  ```

## 解决跨域问题

为什么会有跨域问题，这里就不做详细解释了，可以看一下两篇文章
- [前后端分离djangorestframework——解决跨域请求](https://www.cnblogs.com/Eeyhan/p/10440444.html)
- [Django跨域验证及OPTIONS请求](https://w.url.cn/s/AoDZ2R0)

在settings.py文件中做如下配置

```python
INSTALLED_APPS = [
  ...
  'corsheaders'
  ...
]

MIDDLEWARE = [
  ...
  'corsheaders.middleware.CorsMiddleware', # 注意必须放在CommonMiddleware前面
  ...
]

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = ['*']

CORS_ALLOW_HEADERS = ['*']
```

## jwt登录认证

我们使用rest api接口，一般就很少使用用户名和密码认真，jwt认证是比较常用的，因此这也是项目初始化必须做的。要注意

- 在utils目录下增加auth目录，增加两个文件authentication.py和jwt_util.py

- authentication.py文件

  ```python
  import time
  from django.db.models import Q
  from rest_framework.authentication import BaseAuthentication
  from rest_framework.exceptions import AuthenticationFailed
  from users.models import UserInfo
  from utils.jwt_util import JwtUtil
  from threading import local
  
  _thread_local = local()
  
  class JwtAuthentication(BaseAuthentication):
      def authenticate(self, request):
          access_token = request.META.get('HTTP_ACCESS_TOKEN', None)
          if access_token:
              jwt = JwtUtil()
              data = jwt.check_jwt_token(access_token)
              if data:
                  username = data.get('username')
                  telephone = data.get('telephone')
                  exp = data.get('exp')
                  if time.time() > exp:
                      raise AuthenticationFailed('authentication time out')
  
                  try:
                      user = UserInfo.objects.get(Q(username=username) | Q(telephone=telephone))
                      _thread_local.user = user
                  except (UserInfo.DoesNotExist, UserInfo.MultipleObjectsReturned) as e:
                      return (None, None)
                  else:
                      return (user, None)
  
          raise AuthenticationFailed('authentication failed')
  
  
  def get_current_user():
      return getattr(_thread_local, 'user', None)
  ```

- jwt_util.py文件

  ```python
  import time
  from jose import jwt
  from django.conf import settings
  
  
  class JwtUtil:
      @staticmethod
    def gen_jwt_token(user):
        to_encode = {
            'username': user.username,
            'telephone': user.telephone,
            'exp': time.time() + 24 * 3600,
        }

        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def check_jwt_token(value):
        playload = {}
        try:
            playload = jwt.decode(value, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
                                  )
        except Exception as e:
            logger.exception(e)

        return playload
  ```

- 在settings.py中增加跨域认证的字段

  ```python
  
  REST_FRAMEWORK = {
      'DEFAULT_AUTHENTICATION_CLASSES': [
          'utils.auth.authentications.JwtAuthentication'
      ],
      'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
      'DATETIME_INPUT_FORMATS': '%Y-%m-%d %H:%M:%S'
  }
  ```


## 修改登录认证为JWT方式

- 在utils/auth目录创建user_backend.py文件

  ```python
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
  ```

- 在settings中设置自定义认证方式

  ```python
  AUTHENTICATION_BACKENDS = ['utils.auth.user_backend.UserBackend']
  ```

## Django日志记录

在settings.py中增加如下配置： 

```python
# 日志配置
LOGGER = {
    'maxBytes': '10 MB', # 日志文件大小
    'retention': 5, # 最多记录日志文件数量
    'compression': 'zip', # 历史日志压缩格式
    'level': 'INFO' # 日志级别：INFO、WARNING、ERROR
}

在utils目录下增加logger.py文件

```python
import time
from pathlib import Path
from loguru import logger
from django.conf import settings

log_path = Path(settings.LOG_PATH)

def getLogger(name):
    log_path_info = log_path.joinpath(f'{name}_{time.strftime("%Y-%m-%d")}.log')
    # 日志简单配置 文件区分不同级别的日志
    logger.add(log_path_info,
              rotation=settings.LOGGER.get('maxBytes'),
              encoding='utf-8',
              enqueue=True,
              level=settings.LOGGER.get('level'),
              retention=settings.LOGGER.get('retention'),
              compression=settings.LOGGER.get('compression'))

    return logger

```

在所有需要记录日志的文件中采用如下方式使用

```python
from utils.logger import getLogger


logger = getLogger('auth')

class RegisterView(APIView):
    authentication_classes = []

    def post(self, request):
        ...
        logger.info('用户: %s 注册成功', username)
        ...
```

## 其他

还有一些其他的模块，例如serializers等，整个模板工程我会上传到GitHub上，以供大家参考使用

最后，作为一个模板工程，还欠缺**权限管理**系统，我们后面再完善
