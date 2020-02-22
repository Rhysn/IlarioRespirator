#!/bin/python
# -*- coding:utf-8 -*-


import data.basedata as basedata,data.peopleinfolist as pl
import httpdata.urlinfo as urlinfo, httpdata.httpheader as httpheader
import threading,multiprocessing
import requests
import datetime,time
import random
import pytesseract
from PIL import Image

class appointment(object):

    def __init__(self, url, header, plist, ptime):

        cpu = multiprocessing.cpu_count()

        self.appointment_url = url['appointment']
        self.result_url = url['result']
        self.pic_url = url['picture']
        self.form_url = url['form']

        self.header = header['http_header']
        self.pic_header = header['pic_header']

        self.thrsnum = int(cpu + 1)
        self.procnum = int(cpu / 2 + 1) 
        self.plist = self.formatlist(plist, ptime)
        self.rlist = self.formatrlist(plist)

    def formatlist(self, plist, ptime):

        pl = []
        temppl = []
        date = datetime.date.today() + datetime.timedelta(days=1)
        appodate = date.strftime("%Y-%m-%d")

        for item in plist:
            appo_info = {
                'realname':item['name'],
                'phone':item['phone'],
                'shenfenzheng':item['id'],
                'area':item['areaid'],
                'shop':item['shopid'],
                'pickdate':appodate,
                'shuliang':'5',
                'pid':'1',
                'yzm':''
            }
            temppl.append(appo_info)

        for item_time in ptime:
            for item_info in temppl:
                item_info['picktime'] = item_time
                pl.append(item_info.copy())

        return pl

    def makeappo(self):        
        p = multiprocessing.Pool(self.procnum)
        num = int(len(self.plist) / self.procnum + 1)
        tempList = self.avglist(self.plist, num)
        for item in tempList:
            p.apply_async(self.threadpost, args=(item, self.appointment_url, ))
        p.close()
        p.join()

    def avglist(self, tlist, n):
        for i in range(0,len(tlist),n):
            yield tlist[i : i + n]

    def threadpost(self, plist, url):
        threads = []
        num = int(len(plist) / self.thrsnum) + 1
        tempList = self.avglist(plist, num)
        for item in tempList:
            thread = threading.Thread(target=self.postinfo,args=(url,item,))
            threads.append(thread)
            thread.start()
        for th in threads:
            th.join()

    def postinfo(self, url, info):
        head = {
            'header' : self.header,
            'pic_header' : self.pic_header
            
        }
        
        for item in info:
            try:
                header = self._getheader(head)
                picfile = self._getpicture(header['pic_header'], item['phone'])
                item['yzm'] = str(self._getvcode(picfile))
                re = requests.post(url,data=item.copy(),headers=header['pic_header'])
                print(re.json())
            except ConnectionResetError:
                time.sleep(0.01)
                continue
            else:
                continue

    def getresult(self):
        with open('./result/result.txt' ,'w') as f:
            for item in self.rlist:
                re = requests.post(self.result_url,data=item,headers=self.header)
                f.write(str(re.json())+"\n")
        f.close()

    def formatrlist(self, plist):

        pl = []
        for item in plist:
            appo_info = {
                'realname':item['name'],
                'shenfenzheng':item['id'],
                'pid':'1',
                'result':''
            }
            pl.append(appo_info)

        return pl

    def _getcookies(self):
        try:
            re = requests.get(url=self.form_url)
            while not (re.status_code == 200):
                try:
                    re = requests.get(url=self.form_url)
                except :
                    print(EnvironmentError)
        finally:
            return requests.utils.dict_from_cookiejar(re.cookies)

    def _getheader(self, header):
        cookies = self._getcookies()
        for key in cookies:
            header['header']['cookies'] = key + '=' + cookies[key]
            header['pic_header']['cookies'] = key + '=' + cookies[key]
        return header

    def _getpicture(self, header, fn):
        try:
            re = requests.get(self.pic_url, headers=header)
            while not (re.status_code == 200):
                try:
                    re = requests.get(self.pic_url, headers=header)
                    print(re.content)
                    time.sleep(10)
                except:
                    print(EnvironmentError)                
        finally:
            picfile = r'./data/pictemp/' + fn + r'.png'
            with open(picfile, "wb") as f:
                f.write(re.content) 
        return picfile

    def _getvcode(self, filename):
        fi = Image.open(filename)
        im = fi.convert('L')
        img = im.point(lambda x:255 if x > 128 else 0)
        res = pytesseract.image_to_string(img)
        print(res)

        return res



        

def apporun():
    url = {
        "appointment" : urlinfo.get_appointmenturl(),
        "result" : urlinfo.get_searchurl(),
        "picture" : urlinfo.get_picurl(),
        "form" : urlinfo.get_formurl()
    }

    httpheaders = {
        "http_header" : httpheader.conn_header(),
        "pic_header" : httpheader.pic_header()
    }

    p = pl.peopleinfolist(50)

    plist = p.getpl()
    ptime = basedata.picktime

    appo = appointment(url, httpheaders, plist, ptime)

    date = str(datetime.date.today().strftime("%Y-%m-%d")) + ' 19:45:30'
    temptime = time.strptime(date, "%Y-%m-%d %H:%M:%S")
    keytime = time.mktime(temptime)

    nowtime = time.time()
    fileadd = r'./data/infolist/' + str(nowtime) + r'_plist.txt'
    with open(fileadd ,'w') as f:
        for item in plist:           
            f.write(str(item)+"\n")
    f.close()

    while True:
        appo.makeappo()
        if keytime < time.time():
            break

        


if __name__ == "__main__":

    apporun()

    #appo.getresult()


