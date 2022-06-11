from django.db import models
from django.contrib.auth.backends import UserModel

from demand.models import TblDemand


class TblRecord(models.Model):
    demand = models.ForeignKey(TblDemand, on_delete=models.CASCADE, db_constraint=False)
    opt_type = models.CharField(max_length=16, help_text='操作类型')
    content = models.TextField(help_text='操作内容')
    before_status = models.CharField(max_length=32, help_text='修改前需求状态')
    after_status = models.CharField(max_length=32, help_text='修改前需求状态')
    creator = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING, db_constraint=False, to_field='username')
    create_time = models.DateTimeField(auto_now_add=True, help_text='创建时间')
    
    class Meta:
        db_table = 'tbl_record'
        ordering = ('-create_time',)