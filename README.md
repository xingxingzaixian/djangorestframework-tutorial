最近又开了新项目，后端服务器搭建依然使用我之前一个模板工程，整体我觉得还不错，结构相对清晰一些，最为一个通用的前后端分离后端服务器，还是非常不错的，已经在至少两个项目在使用了。以前我都是把之前的工程删掉逻辑代码，保留部分必要的工程初始化代码。所以就萌生了，把这个模板写下来，传到GitHub上，以备以后直接拉取使用。水平有限、能耐一般，仅代表自己的编程习惯，需要的同学可以参考一下。

需要安装的Python库

- django
- djangorestframework
- django-cors-headers
- Jwt

## 初始化Django工程

```shell
django-admin startproject xingxing
```

创建好工程后，我们要对目录和配置进行一些调整，首先在根目录下创建两个目录：apps和settings，将所有的app都存放到apps目录里面，把settings配置存放在settings目录下，这样我们的根目录就更加清晰了

![image-20200906165728250](https://tva1.sinaimg.cn/large/007S8ZIlly1gih1a24xxyj306z07adg0.jpg)

- 调整settings配置

  首先将xingxing目录下的settings.py文件拷贝到settings目录下，创建dev.py和pro.py两个文件，主要用于开发配置和部署配置，将settings.py文件中的数据库配置和DEBUG移到这两个文件中，内容如下

  ![开发环境配置](https://tva1.sinaimg.cn/large/007S8ZIlly1gih1j0t8hpj30ex07u74s.jpg)

  ![发布环境](https://tva1.sinaimg.cn/large/007S8ZIlly1gih1jrxwzuj30ei081aak.jpg)

  在settings.py文件中把apps添加到环境变量中

  ![image-20200906170827998](https://tva1.sinaimg.cn/large/007S8ZIlly1gih1lhq8acj30gw04fdg5.jpg)

  修改语言和时区

  ![image-20200906171003795](https://tva1.sinaimg.cn/large/007S8ZIlly1gih1n5ltc1j306z02dt8m.jpg)

- 修改manage.py文件

  将Django环境变量设置为开发环境

  ![image-20200906170118839](https://tva1.sinaimg.cn/large/007S8ZIlly1gih1e1vk0cj30jr01h0sr.jpg)

- 修改wsgi.py文件

  将Django环境变量设置为发布环境

  ![image-20200906170235295](https://tva1.sinaimg.cn/large/007S8ZIlly1gih1fdmmknj30l101g0sr.jpg)

## 增加多数据库配置

- 在xingxing目录下增加router.py文件

  路由配置文件当中的返回值是我们在DATABASES中配置的键，默认是default，按照一定的条件返回不同的键，每个键内配置不同的数据库连接，就可以实现Django项目连接多个数据库

  ```python
  class CustomRouter:
      def db_for_read(self, model, **hints):
          return 'default'
  
      def db_for_write(self, model, **hints):
          return 'default'
  
      def allow_relation(self, obj1, obj2, **hints):
          return 'default'
  
      def allow_migrate(self, db, app_label, model_name=None, **hints):
          return 'default'
  ```

- 在settings.py文件中增加路由配置

  ```python
  DATABASE_ROUTERS = ['xingxing.router.CustomRouter']
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
CORS_ALLOW_METHODS = (
  'DELETE',
  'GET',
  'OPTIONS',
  'PATCH',
  'POST',
  'PUT',
  'VIEW',
)

CORS_ALLOW_HEADERS = (
  'XMLHttpRequest', 
  'X_FILENAME',
  'accept-encoding',
  'authorization',
  'content-type',
  'dnt',
  'origin',
  'user-agent',
  'x-csrftoken',
  'x-requested-with',
  'Pragma',
  'access-token'
)
```

## jwt登录认证

我们使用rest api接口，一般就很少使用用户名和密码认真，jwt认证是比较常用的，因此这也是项目初始化必须做的。要注意

- 在根目录下增加utils目录，增加两个文件authentication.py和jwt_util.py

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
  ```

- 在settings.py中增加跨域认证的字段

  ```python
  CORS_ALLOW_HEADERS = (
  	...
    'access-token'
  )
  
  REST_FRAMEWORK = {
      'DEFAULT_AUTHENTICATION_CLASSES': [
          'utils.authentications.JwtAuthentication'
      ],
      'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
      'DATETIME_INPUT_FORMATS': '%Y-%m-%d %H:%M:%S'
  }
  ```


## 修改登录认证为JWT方式

- 在utils目录创建user_backend.py文件

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
  AUTHENTICATION_BACKENDS = ['utils.user_backend.UserBackend']
  ```

## Django日志记录

在settings.py中增加如下配置：

```python
# 日志配置
LOGGING = {
    "version": 1,
    # True表示禁用logger
    "disable_existing_loggers": False,
    'formatters': {
        'default': {
            'format': '%(levelno)s %(module)s %(asctime)s %(message)s ',
            'datefmt': '%Y-%m-%d %A %H:%M:%S',
        },
    },

    'handlers': {
        'request_handlers': {
            'level': 'DEBUG',
            # 日志文件指定为5M, 超过5m重新命名，然后写入新的日志文件
            'class': 'logging.handlers.RotatingFileHandler',
            # 指定文件大小
            'maxBytes': 5 * 1024,
            # 指定文件地址
            'filename': '%s/request.log' % LOG_PATH,
            'formatter': 'default'
        }
    },
    'loggers': {
        'request': {
            'handlers': ['request_handlers'],
            'level': 'INFO'
        }
    },

    'filters': {
        # 过滤器
    }
}
```

在所有需要记录日志的文件中采用如下方式使用

```python
import logging
...

LOG = logging.getLogger('request')

class RegisterView(APIView):
    authentication_classes = []

    def post(self, request):
        ...
        LOG.info('用户: %s 注册成功', username)
        ...
```

## 其他

还有一些其他的模块，例如serializers等，整个模板工程我会上传到GitHub上，以供大家参考使用

最后，作为一个模板工程，还欠缺**权限管理、API文档**系统，我们后面再完善
