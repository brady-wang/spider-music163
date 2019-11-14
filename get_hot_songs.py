import json
from urllib.parse import urlencode

import requests
from lxml import etree
from requests import RequestException

from selenium import webdriver
import time
import csv


# 将获得的歌手的热门歌曲id和名字写入csv文件
def write_to_csv(song_name,song_url):
    csvfile = open('./songs/hotsongs.csv', 'a', encoding='utf-8', newline='')  # 文件存储的位置
    writer = csv.writer(csvfile)
    writer.writerow(('歌曲名称', '歌曲url','评论总数'))



    for name, url in zip(song_name, song_url):
        song_id = url.split('=')[-1]
        url = "https://music.163.com/#" + url
        try:
            if name is not None and url is not None:
                song_comments = get_toal(song_id)

                writer.writerow([name, url,song_comments])
        except Exception as msg:
            print(msg)
            # 当程序的控制流程离开with语句块后, 文件将自动关闭


# 获取歌手id和歌手姓名
def read_csv():

    with open("files/music_163_artists.csv", "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            artist_name, artist_id = row
            if str(artist_id) is "artist_id":
                continue
            else:
                yield artist_name, artist_id
    # 当程序的控制流程离开with语句块后, 文件将自动关闭

def get_toal(music_id):
    para = {
        'offset': 1,  # 页数
        'limit': 20  # 总数限制
    }
    # 歌曲id

    # 歌曲api地址
    musicurl = "http://music.163.com/api/v1/resource/comments/R_SO_4_" + music_id + "?" + urlencode(para)
    # 头结构
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'vjuids=-13ac1c39b.1620457fd8f.0.074295280a4d9; vjlast=1520491298.1520491298.30; _ntes_nnid=3b6a8927fa622b80507863f45a3ace05,1520491298273; _ntes_nuid=3b6a8927fa622b80507863f45a3ace05; vinfo_n_f_l_n3=054cb7c136982ebc.1.0.1520491298299.0.1520491319539; __utma=94650624.1983697143.1521098920.1521794858.1522041716.3; __utmz=94650624.1521794858.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; JSESSIONID-WYYY=FYtmJTTpVwmbihVrUad6u76CKxuzXZnfYyPZfK9bi%5CarU936rIdoIiVU50pfQ6JwjGgBvSyZO0%2FR%2BcoboKdPuMztgHCJwzyIgx1ON4v%2BJ2mOvARluNGpRo6lmhA%5CfcfCd3EwdS88sPgxpiiXN%5C6HZZEMQdNRSaHJlcN%5CXY657Faklqdh%3A1522053962445; _iuqxldmzr_=32',
        'Host': 'music.163.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'
    }

    try:
        response = requests.post(musicurl, headers=headers)

        if response.status_code == 200:
            html = response.content
            data = json.loads(html)  # 将返回的值格式化为json
            return data['total']
    except RequestException:
        print("访问出错")


def main():
    driver = webdriver.Chrome(executable_path="/www/spider-music163/chromedriver")
    for item in read_csv():
        artist_name, artist_id = item
        # 可以任意选择浏览器,前提是要配置好相关环境,更多请参考selenium官方文档
        # 避免多次打开浏览器
        if artist_id != 'artist_id':
            url = "https://music.163.com/#/artist?id=" + str(artist_id)
            print("正在获取{}的热门歌曲...".format(artist_name))
            driver.get(url)
            # 切换成frame
            driver.switch_to_frame("g_iframe")
            # 休眠3秒,等待加载完成!
            time.sleep(3)
            response = driver.page_source

            html = etree.HTML(response)
            song_name = html.xpath("//span[@class='txt']/a/b/@title")
            song_url = html.xpath("//span[@class='txt']/a/@href")

            # 写入到csv文件里面
            write_to_csv(song_name, song_url)
            print("{}的热门歌曲写入到本地成功!".format(artist_name))


if __name__ == "__main__":

    main()
