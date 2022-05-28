#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
路径    : character.py
标题    : 字符处理
创建    : 2022-05-27 10:45
更新    : 2022-05-27 10:45
编写    : 陈倚云
"""
import string
import pinyin


class Character(object):
    """
    字符处理
    """

    @staticmethod
    def get_spell_first(chn_str):
        """
        获取汉字首拼
        """
        spell_first = pinyin.get_initial(chn_str, delimiter="").upper()
        spell_first = spell_first.replace('(', '').replace(',', '').replace(')', '').replace('（', '').replace('）', '').replace('，', '').replace('、', '')
        return spell_first

    @staticmethod
    def str_is_all_chinese(in_str):
        """
        字符串是否全是中文字符
        """
        for ch in in_str:
            if not u'\u4e00' <= ch <= u'\u9fa5':
                return False
        return True

    @staticmethod
    def str_contain_chinese(in_str):
        """
        字符串是否包含中文
        """
        for ch in in_str:
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False

    @staticmethod
    def get_str_chn(in_str):
        """
        提取字符串中的中文字符
        """
        ret_str = ''
        for ch in in_str:
            if u'\u4e00' <= ch <= u'\u9fff':
                ret_str += ch
        return ret_str

    @staticmethod
    def get_chr_style(charactor):
        """
        获取字符类型
        1 中文
        2 英文
        3 英文标点
        4 中文标点
        5 数字
        """
        punc1 = string.punctuation  # 英文标点集合
        punc2 = '！？｡＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏.'  # 中文标点集合
        # 1 如果是中文
        if u'\u4e00' <= charactor <= u'\u9fa5':
            return 1
        elif charactor.isalpha():
            return 2
        elif charactor in punc1:
            return 3
        elif charactor in punc2:
            return 4
        elif charactor.isalnum():
            return 5
        return None