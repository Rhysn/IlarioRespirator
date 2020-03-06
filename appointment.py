#!/bin/python3
# -*- coding:utf-8 -*-


import data.basedata as basedata,data.peopleinfolist as pl
import httpdata.urlinfo as urlinfo, httpdata.httpheader as httpheader
import threading, multiprocessing, requests, datetime, time, random
from PIL import Image
import re as are
import cnn.c_cnn as cnn
import numpy as np
import tensorflow as tf

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

        self.model = cnn.captcha_cnn()
        self.model.load_weights('./cnn/kears_cnn/captcha_cnn_best.h5')
        self.char_set = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def formatlist(self, plist, ptime):
        '''
            格式化信息列表，得到格式如下：
            [
                {
                'shopid': '15', 
                'areaid': '3', 
                'phone': '18654714550', 
                'realname': '罗璐腾', 
                'shenfenzheng': '130105200010126014',
                'shuliang':'5',
                'picktime': '2020-02-20',
                'pickdate': '11:00-13:00',
                'yzm':''
                }
            ]
            截止2020-02-22，数据已不全，还需添加“token”项
        '''

        pl = []
        temppl = []
        #获取明日预约日期
        date = datetime.date.today() + datetime.timedelta(days=1)
        appodate = date.strftime('%Y-%m-%d')

        #填充预约时段外的全部信息
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
                'yzm':'',
                'token':''
            }
            temppl.append(appo_info)
        #填充预约时段信息，保证每人可尝试预约当天全部时段
        for item_time in ptime:
            for item_info in temppl:
                item_info['picktime'] = item_time
                pl.append(item_info.copy())

        return pl

    def makeappo(self):
        '''
            创建进程池，采用多进程形式尝试预约
        '''
        p = multiprocessing.Pool(self.procnum)
        num = int(len(self.plist) / self.procnum + 1)
        #根据所创建进程数量，拆分数据列表，每组数量为num，最后一组可能少于num；
        tempList = self.avglist(self.plist, num)
        for item in tempList:
            p.apply_async(self.threadpost, args=(item, self.appointment_url, ))
        p.close()
        p.join()

    def avglist(self, tlist, n):
        '''
            以步长n拆分列表
        '''
        for i in range(0,len(tlist),n):
            yield tlist[i : i + n]

    def threadpost(self, plist, url):
        '''
            创建子线程，并根据线程数量拆分数据列表
        '''
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
        '''
            向服务器发送POST请求，完成预约
        '''
        head = {
            'header' : self.header,
            'pic_header' : self.pic_header
            
        }        
        for item in info:
            try:
                #获取header信息，用以获取验证码、提交预约申请，cookies实时更新
                header, token = self._getheaderandtoken(head)
                #获取验证码图片
                picpath = self._getpicture(header['pic_header'], item['phone'])
                #识别验证码，填充数据
                item['yzm'] = str(self._getvcode(picpath))
                item['token'] = token
                re = requests.post(url,data=item.copy(),headers=header['pic_header'])
                print(re.json())
            except ConnectionResetError:
                time.sleep(0.01)
                continue
            else:
                continue

    def getresult(self):
        '''
            查询预约结果，并保存
        '''
        with open('./result/result.txt' ,'w') as f:
            for item in self.rlist:
                re = requests.post(self.result_url,data=item,headers=self.header)
                f.write(str(re.json())+'\n')
        f.close()

    def formatrlist(self, plist):
        '''
            格式化结果查询列表
        '''
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

    def _getcookiesandtoken(self):
        '''
            获取cookies及token
            后续使用此cookies获取验证码
        '''
        try:
            re = requests.get(url=self.form_url)
            while not (re.status_code == 200):
                try:
                    re = requests.get(url=self.form_url)
                    pattern = are.compile(r"var token = \S+';")
                    token = pattern.search(re.text)
                    token = token.group(0).split("'")
                except :
                    print(EnvironmentError)
        finally:
            return requests.utils.dict_from_cookiejar(re.cookies), token

    def _getheaderandtoken(self, header):
        '''
            完善header信息
        '''
        cookies, token = self._getcookiesandtoken()
        for key in cookies:
            header['header']['cookies'] = key + '=' + cookies[key]
            header['pic_header']['cookies'] = key + '=' + cookies[key]
        return header, token

    def _getpicture(self, header, fn):
        '''
            请求验证码刷新，并保存验证码图片
        '''
        try:
            re = requests.get(self.pic_url, headers=header)
            while not (re.status_code == 200):
                try:
                    re = requests.get(self.pic_url, headers=header)
                except:
                    print(EnvironmentError)                
        finally:
            picfile = r'./data/pictemp/' + fn + r'.png'
            with open(picfile, 'wb') as f:
                f.write(re.content) 
        return picfile

    def _getvcode(self, picpath):
        '''
            处理验证码图片，并识别验证码
            cnn模型训练程度极低，999条基础数据
        '''
        data_x = np.zeros((1, 25, 80, 3))
        x = tf.io.read_file(picpath)        
        x = tf.image.decode_png(x, channels=3)
        x = tf.image.convert_image_dtype(x, tf.float64)             
        x /= 255.
        x = tf.reshape(x, (25, 80, 3))

        data_x[0, :] = x
        prediction_value = self.model.predict(data_x)
        res = self.vec2text(np.argmax(prediction_value, axis=2))

        return res

    def vec2text(self, vec):
        text = []
        for item in vec:
            index = item[0]
            text.append(self.char_set[index])
        return ''.join(text)



        

def apporun():
    url = {
        'appointment' : urlinfo.get_appointmenturl(),
        'result' : urlinfo.get_searchurl(),
        'picture' : urlinfo.get_picurl(),
        'form' : urlinfo.get_formurl()
    }

    httpheaders = {
        'http_header' : httpheader.conn_header(),
        'pic_header' : httpheader.pic_header()
    }

    #随机创建50人的个人信息，包括身份证号、手机号、姓名
    p = pl.peopleinfolist(50)
    plist = p.getpl()
    ptime = basedata.picktime

    appo = appointment(url, httpheaders, plist, ptime)

    #设计停止预约时间标志
    date = str(datetime.date.today().strftime('%Y-%m-%d')) + ' 19:45:30'
    temptime = time.strptime(date, '%Y-%m-%d %H:%M:%S')
    keytime = time.mktime(temptime)

    #使用时间戳为名保存所创建的身份信息，方便后续查询预约结果
    nowtime = time.time()
    fileadd = r'./data/infolist/' + str(nowtime) + r'_plist.txt'
    with open(fileadd ,'w') as f:
        for item in plist:           
            f.write(str(item)+'\n')
    f.close()

    while True:
        appo.makeappo()
        if keytime < time.time():
            break

        


if __name__ == '__main__':

    apporun()

    #appo.getresult()


