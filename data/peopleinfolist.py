# !/user/bin/python
# -*- coding:utf-8 -*-

import random,threading


class peopleinfolist():
	
    def __init__(self, num):
        self.num = num
        self.pl = []
        self.idl = []
        self.namel = []
        self.phonel = []
        self.peoil = []

        #创建多线程，完成身份证、手机号、姓名、预约门店信息的随机生成且不重复
        tid = threading.Thread(target=self._getid, args=())
        tname = threading.Thread(target=self._getname, args=())
        tshop = threading.Thread(target=self._getshop, args=())
        tphone = threading.Thread(target=self._getphone, args=())

        tid.start()
        tname.start()
        tshop.start()
        tphone.start()

        tid.join()
        tname.join()
        tshop.join()
        tphone.join()

        self._makepeopleinfolist()


    def _getid(self):
        '''
            生成随机身份证号码，不考虑不同月份天数不同的影响；
            只随机日期在28以内的
        '''
        placenums = ['130102','130104','130105','130107','130108','130109','130110']
        weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        cheack_code = {'0': '1','1': '0','2': 'X','3': '9','4': '8','5': '7','6': '6','7': '5','8': '4','9': '3','10': '2'}

        ids = set()

        while len(ids) < self.num:
            placenum = random.choice(placenums)

            year = str(random.randint(1963,2011))
            m = random.randint(1,12)
            month = str(m) if m > 9 else ('0' + str(m))
            d = random.randint(1,28)
            day = str(d) if d > 9 else ('0' + str(d))
            date = year + month + day

            ID_former = placenum + date + str(random.randint(100,999))

            sum = 0
            for i, num in enumerate(ID_former):
                sum += int(num) * weight[i]

            ID_check = cheack_code[str(sum % 11)]
            ids.add(ID_former + ID_check)

        self.idl = list(ids)
		
    def _getname(self):
        #随机生成人员姓名
        firstnames = [
                        '张','白','林','杨','刘','梁','苏','石','赛','尚','丁','董','王',
                        '戴','段','方','范','冯','高','郭','许','徐','聂','黄','赵','周',
                        '章','陈','曾','牛','朱','钟','韩','包','吕','展','魏','金','童',
                        '顾','孙','郑','胡','邓','左','靳','闻','葛','司','田','吴','马',
                        '卞','崔','甄','曹','杜','郝','吕','毛','任','潘','谢','姜','武',
                        '袁','尹','于','何','叶','薛','要','宁','耿','司马','上官','欧阳',
                        '次','冉','艾','诸葛','孔','夏','沙','齐','江','贾','连','秦',
                        '侯','孟','卢','贾','邵','蔡','程','万','姚','罗','韦','唐','朗',
                        '贺','沈','汤','佟','慕','闫','谭','陆','艾','祁','丰','古','娄',
                        '洪','侯'
                    ]
        lastnames = [
                        '水','静','敏','聪','辉','慧','淼','永','国','刚','强','风','花',
                        '雪','月','涛','海','萍','晶','丽','利','峰','明','星','兴','乐',
                        '龙','旺','易','婉','楠','笑','霞','光','彩','才','益','帅','琳',
                        '晓','雅','俊','军','赫','凯','耀','杰','芳','航','达','垣','屹',
                        '珊','姗','彬','斌','益','秀','玲','松','铭','洲','亚','叶','文',
                        '娟','玉','婷','博','礼','莉','莹','梦','英','雄','珑','烟','泰',
                        '晨','光','志','智','珉','烨','贤','阳','洋','安','康','翔','丰',
                        '飞','伟','威','薇','娜','冰','霜','浅','清','琴','勤','亮','晴',
                        '青','庆','柳','秋','语','荣','智','志','念','缘','羽','柔','婕',
                        '杉','缤','梅','彤','盛','硕','琼','宁','豪','华','欣','坤','璐',
                        '襄','超','川','宇','柏','贝','慈','睿','瑞','祥','树','兰','岚',
                        '旭','芝','诺','佳','嘉','雨','天','娟','鸿','璐','航','澜','忠',
                        '富','福','悦','越','超','艺','栋','毅','冰','歌','芬','芳','浩',
                        '腾','鑫','蕾','雷','帆','鹏','雷','烟','桃','舟','茜','策','露',
                        '欢','心','一','初','涵','然','璇','颖','腾','蓬','娥','琪','琦',
                        '新','淑','军','君','娇','莎','倩','窈','窕','茗','恒','萱','珍',
                        '昭','朝','宝','萌','楚','瑛','滢','菲','翠','远','云','韵','运',
                        '浮','笙','苼','仙','世','和','碧','靖','菁','宗','剑','河','谨',
                        '义','彦','家','佳','辰','舒','香','茹','柯','德','燕','影','敬',
                        '景','雯','磊','','','','','','','','','','','','','','','','',
                        '','','','','','','','','','','','','','','','','','','','',''
                    ]
        names = set()
		
        while len(names) < self.num:
            name = random.choice(firstnames) + random.choice(lastnames) + random.choice(lastnames)
            if len(name) > 1:
                names.add(name)
			
        self.namel = list(names)
		
    def _getphone(self):
        #生成手机号
        phsegment = [
                        '136','139','151','133','156','155','130','177','173','172','188','178','132',
                        '180','150','189','185','186','137','159','131'
                    ]
        phones = set()
        while len(phones) < self.num:
            phone = str(random.choice(phsegment)) + str(random.randint(32567112,99998698))
            phones.add(phone)
			
        self.phonel = list(phones)

    def _getshop(self):
        '''
            随机生成门店及区域信息，信息不全
        '''
        shops = [
                {"shopid":"15","areaid":"3"},{"shopid":"18","areaid":"15"},{"shopid":"20","areaid":"15"},
                {"shopid":"23","areaid":"15"},{"shopid":"36","areaid":"15"},{"shopid":"37","areaid":"15"},
                {"shopid":"38","areaid":"15"},{"shopid":"50","areaid":"15"},{"shopid":"60","areaid":"15"}
        ]

        num = self.num
        while num:
            num -= 1
            self.pl.append(random.choice(shops)) 

    def _makepeopleinfolist(self):
        '''
            使用所生成的随机数据创建人员信息列表
        '''

        for index, item in enumerate(self.pl):
            item['phone'] = self.phonel[index]
            item['name'] = self.namel[index]
            item['id'] = self.idl[index]
            item['yzm'] = ''
            self.peoil.append(item.copy())

    def getpl(self):
        return self.peoil
