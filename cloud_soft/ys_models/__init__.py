#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
路径    : __init__.py.py
标题    : 抽象模型和模型管理器
创建    : 2022-05-29 8:54
更新    : 2022-05-29 8:54
编写    : 陈倚云
"""
import json
import operator
import re
from django.db import models

class BaseAbsModel(models.Model):
    """
    基础抽象模型
    1 用于其它抽象模型的基类
    2 用于系统自动产生的数据
    """

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        abstract = True


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

class ModelManage(models.Manager):
    """
    基础抽象模型管理器
    """
    _page_cnt = 50

    def sql_browse_lst(self, q=None, record_id=None, page_num=None, field_fun=None, fun_q=None):
        """
        浏览列表
        :param q: 查询条件
        :param record_id: 当前选中id
        :param page_num: 当前页 用于分页显示
        :param field_fun: 返回函数名 调用返回函数
        :param fun_q: 返回函数参数
        """
        # 1 生成条件过滤数据
        if q is None:
            objs = super(ModelManage, self).get_queryset().all()
        else:
            objs = super(ModelManage, self).get_queryset().filter(q)
        # 2 生成分页数据
        page_num = 1 if page_num is None else int(page_num)
        start = (page_num - 1) * self._page_cnt
        end = page_num * self._page_cnt
        objs = objs[start:end]
        # 3 生成默认选项
        info = dict()
        if fun_q is not None:
            f = operator.methodcaller(field_fun, fun_q)
        else:
            f = operator.methodcaller(field_fun)
        if record_id is not None:
            selected = super(ModelManage, self).get_queryset().get(id=record_id)
            select_dct = f(selected)
            info.update(selected=select_dct)
        # 5 生成列表数据
        info_lst = []
        for obj in objs:
            inf_dct = f(obj)
            if record_id is not None:
                checked = 2 if obj.id == record_id else 0
                inf_dct.update(checked=checked)
            info_lst.append(inf_dct)
        info.update(data_lst=info_lst)

        return info

    def _filter_q(self, q):
        """
        处理条件过滤
        """
        if q is None:
            records = super(ModelManage, self).get_queryset().all()
        else:
            records = super(ModelManage, self).get_queryset().filter(q)
        return records

    def _filter_page(self, records, page_num):
        if page_num is None:
            page_num = 1
        start_num = (page_num - 1) * self._page_cnt
        end_num = page_num * self._page_cnt
        records = records[start_num:end_num]
        return records

    def _filter_lst(self, records, page_num, selected_lst, field_fun):
        records = self._filter_page(records, page_num)
        f = operator.methodcaller(field_fun)
        data_lst = []
        selected_lst = [] if selected_lst is None else selected_lst
        for record in records:
            info = f(record)
            if len(selected_lst) > 0:
                selected = True if record.id in selected_lst else False
                info.update(checked=selected)
            data_lst.append(info)
        return data_lst

    def _filter_tab(self, records, tab_fields, tab_index, page_num, field_fun):
        """
        处理tab过滤
        """
        tabs = []
        data_lst = []
        tab_index = 1 if tab_index is None else int(tab_index)
        for ti, tab_field in enumerate(tab_fields):
            que = models.Q()
            que.connector = 'AND'
            que.children.append(tab_field[:2])
            tab_items = records.filter(que)
            tabs.append({
                'tab_name': tab_field[2],
                'lst_cnt': len(tab_items),
                'tab_index': ti + 1,
                'selected': True if tab_index == ti + 1 else False
            })
            if tab_index - 1 == ti:
                objs = self._filter_page(tab_items, page_num)
                f = operator.methodcaller(field_fun)
                for obj in objs:
                    data_lst.append(f(obj))
        info = {
            'tabs': tabs,
            'data_lst': data_lst
        }
        return info

    def _get_selected_lst(self, selected_lst, field_fun):
        records = super(ModelManage, self).get_queryset().filter(id__in=selected_lst)
        sel_lst = []
        f = operator.methodcaller(field_fun)
        for record in records:
            sel_lst.append(f(record))
        return sel_lst

    def sql_lst(self, q=None, tab_fields=None, tab_index=None, page_num=None, selected_lst=None, field_fun=None):
        """
        查询列表
        :param tab_fields:分组列表 用于分组显示
        :param tab_index: 当前分组 用于分组显示
        :param q: 查询条件
        :param page_num: 当前页 用于分页显示
        :param selected_lst: 选中记录 用于查询时默认选中
        :param field_fun: 返回函数名 调用返回函数
        :return:
        """
        ret_info = dict()
        records = self._filter_q(q)
        if tab_fields is None:
            if selected_lst is not None and len(selected_lst) > 0:
                sel_lst = self._get_selected_lst(selected_lst, field_fun)
                ret_info.update(selected_lst=sel_lst)
            info = self._filter_lst(records, page_num, selected_lst, field_fun)
            ret_info.update(data_lst=info)
        else:
            info = self._filter_tab(records, tab_fields, tab_index, page_num, field_fun)
            ret_info.update(info)
        return ret_info

    def _init_update_info(self, info):
        """
        初始化上传数据
        """
        fields = self.model._meta.fields
        key_lst = []  # 用于存放当前模型中所有字段
        text_lst = []  # 用于存放当前模型中类型为TextField的字段
        for field in fields:
            # 获取当前模型中所有的字段名,其中一对多名一对一的字段名必须增加_id
            if type(field).__name__ == 'ForeignKey' or type(field).__name__ == 'OneToOneField':
                key_word = str(field.name) + '_id'
            else:
                key_word = str(field.name)
            key_lst.append(key_word)
            # 获取TextField字段名,因为该字段需要用json来转换。
            if type(field).__name__ == 'TextField':
                text_lst.append(str(field.name))
        # 移除提交字段中的无用字段,即表中没有的字段
        pop_lst = []  # 用于存放提交字段中的无用字段
        for key in info:
            if str(key) not in key_lst:
                pop_lst.append(str(key))
        for item in pop_lst:
            info.pop(item)
        # 初始化上传数据
        for key in info:
            # 如果该字段为None或该字段长度为0,则置为空
            if info[key] is None or len(str(info[key]).strip()) == 0:
                info[key] = None
            # 对TextField字段,如果不为空,则转换编码后存储
            if key in text_lst:
                if info[key] is not None:
                    info[key] = json.dumps(str(info[key]))
        return info

    def _get_record_id(self, info):
        """
        获取当前欲更新的记录id,None表示新增,否则更新
        """
        name_lst = ([a for a in re.split(r'([A-Z][a-z]*)', self.model.__name__) if a])
        id_name = ''
        for name in name_lst:
            if len(id_name) == 0:
                id_name = name.lower()
            else:
                id_name += '_' + name.lower()
        id_name += '_id'
        record_id = None if info.get(id_name, None) is None or len(str(info[id_name]).strip()) == 0 else int(info[id_name])
        return record_id

    def save(self, info):
        """
        保存数据
        """
        record_id = self._get_record_id(info)
        info = self._init_update_info(info)
        if record_id is None:
            obj = self.model.objects.create(**info)
            # obj.save()
        else:
            objs = self.model.objects.filter(id=record_id)
            objs.update(**info)
            obj = objs[0]
        return obj

    def stick(self, record_id, q=None):
        """
        置顶:按当前的order重新分配
        """
        if q is None:
            curr_record = super(ModelManage, self).get_queryset().filter(id=record_id).first()
        else:
            curr_record = super(ModelManage, self).get_queryset().filter(q).filter(id=record_id).first()
        if curr_record is not None:  # 如果当前记录存在
            if curr_record.order > 0:  # 1 如果已经置顶了,则取消置顶
                curr_record.order = 0
                curr_record.save()
            else:  # 2 如果未置顶,则置顶
                if q is None:
                    records = super(ModelManage, self).get_queryset().filter(order__gt=0)
                else:
                    records = super(ModelManage, self).get_queryset().filter(q).filter(order__gt=0)
                print(len(records))
                if len(records) > 0:  # 如果有其它置顶记录,则把其它置顶记录+1
                    for record in records:
                        record.order -= 1
                        record.save()
                curr_record.order = 9223372036854775806  # 先置顶
                curr_record.save()
        return record_id