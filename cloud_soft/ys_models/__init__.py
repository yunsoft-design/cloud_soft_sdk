#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
路径    : __init__.py.py
标题    : 抽象模型和模型管理器
创建    : 2022-05-29 8:54
更新    : 2022-05-29 8:54
编写    : 陈倚云
"""
import time

from django.db import models
from .ys_models_manager import YsModelsManager
from cloud_soft.ys_transition import YsTransition


class BaseAbsModel(models.Model):
    """
    基础抽象模型
    1 用于其它抽象模型的基类
    2 用于系统自动产生的数据
    """
    objects = YsModelsManager()
    id = models.BigIntegerField(primary_key=True)
    # 因id即为创建时间戳,所以,不需要创建时间字段
    # create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        保存
        """
        if self.id is None:
            self.id = YsTransition.dec_to_sixty_two(int(time.time() * 10000000))
        super().save(*args, **kwargs)


class CommonAbsModel(BaseAbsModel):
    """
    常用抽象模型
    1 用于其它抽象模型继承
    2 用于用户录入的数据
    """
    IS_VALID = (
        (False, '禁用'),
        (True, '启用'),
    )
    create_user = models.BigIntegerField(null=True, verbose_name='创建人id')
    update_user = models.BigIntegerField(null=True, verbose_name='更新人id')
    order = models.BigIntegerField(default=0, verbose_name='顺序号')
    valid_user = models.BigIntegerField(null=True, verbose_name='设置人')
    is_valid = models.BooleanField(choices=IS_VALID, default=True, verbose_name='有效标志')  #
    remark = models.CharField(max_length=200, null=True, verbose_name='备注')

    class Meta:
        abstract = True


class AuditAbsModel(CommonAbsModel):
    """
    审核抽象模型
    用于需要审核的模型
    """
    AUDIT_STATUS = (
        (0, '未申请'),
        (1, '已申请'),
        (2, '已审核'),
        (3, '已驳回'),
    )
    audit_status = models.SmallIntegerField(choices=AUDIT_STATUS, default=0, verbose_name='审核状态', blank=True)
    apply_user = models.BigIntegerField(null=True, verbose_name='申请人')
    audit_user = models.BigIntegerField(null=True, verbose_name='审核人')

    class Meta:
        abstract = True
