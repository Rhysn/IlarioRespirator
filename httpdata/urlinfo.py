#!/bin/python
# -*- coding:utf-8 -*-
__name__ = 'urlinfo'


appointment_url = r'http://lerentang.yihecm.com/?m=save'
search_url = r'http://lerentang.yihecm.com/?m=resultchaxun'
pic_url = r'http://lerentang.yihecm.com/core/common/yzm.php?0.29450912268882457'
form_url = r'http://lerentang.yihecm.com/?m=yuyuelist&id=1'

def get_appointmenturl():
    return appointment_url

def get_searchurl():
    return search_url

def get_picurl():
    return pic_url

def get_formurl():
    return form_url