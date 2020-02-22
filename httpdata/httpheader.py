#!/bin/python
# -*- coding:utf-8 -*-
__name__ = 'httpheader'

def conn_header():
    header = {
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-cn',
        'Connection':'close',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie':'PSESSID=fkg7p3icjjs80sjq1k1484mdg4',
        'Host':'lerentang.yihecm.com',
        'Origin':'http://lerentang.yihecm.com',
        'Referer':'http://lerentang.yihecm.com/?m=yuyuelist&id=1',
        'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.10(0x17000a21) NetType/WIFI Language/zh_CN',
        'X-Requested-With':'XMLHttpRequest'
    }

    return header

def pic_header():
    header = {
        "Accept": "image/png,image/svg+xml,image/*;q=0.8,video/*;q=0.8,*/*;q=0.5", 
        "Accept-Encoding": "gzip, deflate", 
        "Accept-Language": "zh-cn", 
        "Connection": "close", 
        "Cookie": "PHPSESSID=fkg7p3icjjs80sjq1k1484mdg4", 
        "Host": "lerentang.yihecm.com", 
        "Referer": "http://lerentang.yihecm.com/?m=yuyuelist&id=1", 
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.10(0x17000a21) NetType/WIFI Language/zh_CN"
    }

    return header

def default_header():
    header = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 
        "Accept-Encoding": "gzip, deflate", 
        "Accept-Language": "zh-cn", 
        "Connection": "close", 
        "Cookie": "PHPSESSID=frmecrb4vsc7g1pf12f81qcej1", 
        "Host": "lerentang.yihecm.com", 
        "Referer": "http://lerentang.yihecm.com/?m=list", 
        "Upgrade-Insecure-Requests": "1", 
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.10(0x17000a21) NetType/WIFI Language/zh_CN"
    }

    return header