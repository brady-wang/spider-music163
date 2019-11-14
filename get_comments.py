# -*- coding: utf-8 -*-
# @Time    : 2018/3/15 15:27
# @Author  : XueLei
# @Site    :
# @File    : neteasemusic.py
# @Software: PyCharm
#抓取某一首歌下面的评论

import requests
from requests.exceptions import RequestException
from urllib.parse import urlencode
import json
from multiprocessing import Pool#多进程池

def get_response(offset,limit):
    #参数
    para = {
        'offset':offset,#页数
        'limit':limit#总数限制
    }
    # 歌曲id
    musicid = "520458203"  # 《大学无疆》
    #歌曲api地址
    musicurl = "http://music.163.com/api/v1/resource/comments/R_SO_4_"+musicid+"?"+urlencode(para)
    #头结构
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Cookie':'vjuids=-13ac1c39b.1620457fd8f.0.074295280a4d9; vjlast=1520491298.1520491298.30; _ntes_nnid=3b6a8927fa622b80507863f45a3ace05,1520491298273; _ntes_nuid=3b6a8927fa622b80507863f45a3ace05; vinfo_n_f_l_n3=054cb7c136982ebc.1.0.1520491298299.0.1520491319539; __utma=94650624.1983697143.1521098920.1521794858.1522041716.3; __utmz=94650624.1521794858.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; JSESSIONID-WYYY=FYtmJTTpVwmbihVrUad6u76CKxuzXZnfYyPZfK9bi%5CarU936rIdoIiVU50pfQ6JwjGgBvSyZO0%2FR%2BcoboKdPuMztgHCJwzyIgx1ON4v%2BJ2mOvARluNGpRo6lmhA%5CfcfCd3EwdS88sPgxpiiXN%5C6HZZEMQdNRSaHJlcN%5CXY657Faklqdh%3A1522053962445; _iuqxldmzr_=32',
        'Host':'music.163.com',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'
    }
    #代理IP
    proxies= {
        'http:':'http://121.232.146.184',
        'https:':'https://144.255.48.197'
    }
    try:
        response = requests.post(musicurl,headers=headers,proxies=proxies)
        if response.status_code == 200:
            return response.content
    except RequestException:
        print("访问出错")

#解析返回页
def parse_return(html):
    data = json.loads(html)#将返回的值格式化为json
    if data.get('hotComments'):
        hotcomm = data['hotComments']
        print('--------------------------------------------------------------这是热门评论-------------------------------------------------------------------------------')
        for hotitem in hotcomm:
            hotdata = {
                '用户名': hotitem['user']['nickname'],
                '用户头像': hotitem['user']['avatarUrl'],
                'content': hotitem['content'],
                '赞':hotitem['likedCount']
            }
            print(hotdata)
        print('------------------------------------------------------------------------------------------------------------------------------------------------------------')
    # else:
    #     print('--------------------------------------------------')
    if data.get('comments'):
        comm = data['comments']
        for item in comm:
            data = {
                '用户名': item['user']['nickname'],
                '用户头像': item['user']['avatarUrl'],
                'content': item['content'].replace('\r', ' '),
                '赞': item['likedCount']
            }
            print(data)
        print('-------------------------------------------------------------------------------------------------------------------------------------------------------------')
def main(offset):
    gethtml = get_response(offset,200)
    parse_return(gethtml)

if __name__ == '__main__':
    # groups = [x*20 for x in range(0,20)]
    # pool = Pool()
    # pool.map(main,groups)
    for x in range(0,20):
        main(x*20)