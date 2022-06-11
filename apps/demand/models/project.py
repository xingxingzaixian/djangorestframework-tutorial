from django.db import models
from django.contrib.auth.backends import UserModel


class TblProject(models.Model):
    name = models.CharField(max_length=64, unique=True, help_text='项目名称')
    version = models.CharField(max_length=64, help_text='项目版本')
    parent = models.ForeignKey('self',
                              related_name='children',
                              on_delete=models.SET_NULL,
                              blank=True,
                              null=True,
                              db_constraint=False,
                              help_text='父级')
    delay = models.BooleanField(default=False, help_text='是否延期')
    description = models.TextField(blank=True, null=True, help_text='项目描述')
    status = models.CharField(max_length=32, default='plan', help_text='项目状态')
    creator = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING, db_constraint=False, to_field='username')
    leader = models.CharField(max_length=64, default='', help_text='负责人')
    start_date = models.DateField(help_text='开始日期')
    end_date = models.DateField(help_text='结束日期')
    create_time = models.DateTimeField(auto_now_add=True, help_text='创建时间')
    finish_time = models.DateTimeField(blank=True, null=True, help_text='完成时间')
  
    class Meta:
        db_table = 'tbl_project'
        ordering = ('-create_time',)