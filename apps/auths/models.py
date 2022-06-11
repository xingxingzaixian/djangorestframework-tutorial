from django.db import models


class TblRole(models.Model):
    name = models.CharField(max_length=64, help_text='角色')
    desc = models.CharField(max_length=256, help_text='描述')

    class Meta:
        db_table = 'tbl_role'
        