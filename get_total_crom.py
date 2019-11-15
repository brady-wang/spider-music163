# -*- coding: utf-8 -*-
# @Time    : 2018/3/15 15:27
# @Author  : XueLei
# @Site    :
# @File    : neteasemusic.py
# @Software: PyCharm
# 抓取某一首歌下面的评论
import time
from lxml import etree

import requests
from requests.exceptions import RequestException
from urllib.parse import urlencode
import json
from multiprocessing import Pool  # 多进程池

from selenium import webdriver


def main(music_id):
    driver = webdriver.Chrome(executable_path="/www/spider-music163/songs/chromedriver.exe")

    # 可以任意选择浏览器,前提是要配置好相关环境,更多请参考selenium官方文档
    # 避免多次打开浏览器
    url = "https://music.163.com/#/song?id=" + str(music_id)
    print("正在获取{}的评论 ...".format(music_id))
    driver.get(url)
    # 切换成frame
    driver.switch_to_frame("g_iframe")
    # 休眠3秒,等待加载完成!
    time.sleep(3)
    response = driver.page_source

    html = etree.HTML(response)
    total = html.xpath("//span[@class='j-flag']/text()")
    print(total)




if __name__ == "__main__":
    music_id = 513360721
    main(music_id)
