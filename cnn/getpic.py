    
import requests    
    
    
    
class getpic():
    def __init__(self, pic_url):
        self.pic_url = pic_url
        pass

    def getpicture(self, header, fn):
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
            picfile = r'./pictemp/' + fn + r'.png'
            with open(picfile, "wb") as f:
                f.write(re.content) 
        return picfile


if __name__ == "__main__":
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

    pic_url = r'http://lerentang.yihecm.com/core/common/yzm.php?0.29450912268882457'

    pic = getpic(pic_url)

    for i in range(1000):
        pic.getpicture(header, str(i))