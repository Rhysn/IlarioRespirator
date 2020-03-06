# IlarioRespirator


乐仁堂口罩预约脚本

本脚本用于乐仁堂口罩的预约，未做测试。
使用正则匹配填充token内容
使用CNN解决验证码识别问题，目前受限于训练集过小，训练程度有限。

## 内容列表

- [安装](#安装)
- [使用](#使用说明)
- [文件说明](#文件说明)
- [使用许可](#使用许可)

## 安装

本项目使用 [Python3](https://www.python.org/) 进行实现，需安装Python3后运行。

## 使用说明

可直接通过如下语句执行。

```python
$ python appointmen.py
# 默认随机生成50人信息并进行尝试预约
```
## 文件说明


pages中为2020-02-22抓取的 [口罩预约](http://lerentang.yihecm.com/?m=yuyuelist&id=1) 页面内容



## 使用许可

[Apache License 2.0](https://github.com/Rhysn/IlarioRespirator/blob/master/LICENSE) © Richard Littauer

