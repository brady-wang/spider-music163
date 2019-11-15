import json
from urllib.parse import urlencode

import requests
from lxml import etree
from requests import RequestException

from selenium import webdriver
import time
import csv





# 获取歌手id和歌手姓名
def read_csv():
    with open("files/music_163_artists2.csv", "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            artist_name, artist_id = row
            if str(artist_id) is "artist_id":
                continue
            else:
                yield artist_name, artist_id
    # 当程序的控制流程离开with语句块后, 文件将自动关闭

def get_total1(music_id,song_name):
    # 参数
    para = {
        'offset': 1,  # 页数
        'limit': 10  # 总数限制
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
        'Cookie': 'mail_psc_fingerprint=694536e51b64297a4c006d945e3e5ca6; _iuqxldmzr_=32; _ntes_nnid=5908c649eb7f3f30391520e056dcb60d,1569936932455; _ntes_nuid=5908c649eb7f3f30391520e056dcb60d; playliststatus=visible; WM_TID=YkjANYcfFZxEUVEBFAY84sQ7wJCALTV5; NTES_SESS=.3Vbv1oMsRu67NWwlFp0p15o40S_wjrd2j5Rc38DQFb9krW0kCD17o72UXWbiEcoKwmIvGyqlJ.PQydEbaHjgAtktl87ud9vzjL2QdWh0mD2YW7euNGImuK1VHGO5IQOP1k0muQWsrbuph48Y5Cb_I449rnWDqMRb_MuoZ8bTrT2Evt0oQcXH_OSDX6JIhrh7SIN5NzTzFLOFSh0XAPVyE6bt; S_INFO=1570269261|0|3&80##|wys1749#feng_xing_tian_xia#hxl2219; P_INFO=wys1749@163.com|1570269261|0|other|00&99|gud&1570268620&carddav#gud&440300#10#0#0|158692&0|mail163&mail163_chg|wys1749@163.com; ANTICSRF=838280eb85b442e9a64ff30402d81b67; MUSIC_EMAIL_U=ce9a5dfc7c3300d2c5d2e02a51e5f2ae3c58347bd3bf127748dc522e193e020cb537658fb98ad9f6857dab8821efcea010fe0eca6d1cd081c3061cd18d77b7a0; WM_NI=G%2BIwSnE5cqwvKVIlB9hMIbOP2naBosLcsTipnDjBXhz8KmrR3oSPf%2B8HiAPVdRfnBLLhWRvV9hkCa7ywIrvqNz5bEmWI7cxh5CjfTm%2FtC2PswNLYPiEnDxvZkpsvWck5Mms%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eeb7f2428bb19796ef64a6e78ea3d45a978f8b84b83e9cb79995b83381eca98ab72af0fea7c3b92a85f58798d26687ebad92f67e898a878dc133ac938783ce5cf2b2afa3ee7990bdbdb5ec7cae9ca6a3db64bae8858ef15af1b19db1e521fc98a7a2d35ea88eaa8fc14890b899b3f55efbb8a5a4e43dbba98793f57b8ea6fb83c8679597f984fb64f79da687d767edac8dd3d379b59284bad36387b28c99f552a9b0bd97d669a9eb838ef237e2a3; MUSIC_FU=18ebf347f72f45e068dbb4c7ea45ac7eb34c3df2dac3d0abca3a437ab0766a6c; __remember_me=true; ntes_kaola_ad=1; __51cke__=; JSESSIONID-WYYY=5x5rNgX8qws%5Cg7xQ7ZKFea8raAoljESQX9w%2BZM%5CltbzJ8QAQg%2F%5C6xyQWqU1kPaFVQmy%2BSZqQZiXIvsqv926uWsc%2FlvVWYnZgA2KSlUyl6yGaOrcBZFkMfv7GmWGuWRPvozpv2V7zlqJWyTI9jNpna%2BYDDWo78E4Q54Xd5YKK4IRjY0lr%3A1573742759250; __tins__19988117=%7B%22sid%22%3A%201573740961411%2C%20%22vd%22%3A%203%2C%20%22expires%22%3A%201573742964989%7D; __51laig__=4; playerid=11702233; MUSIC_U=c4c359dd3b2dd080aa438c2824b5d282d0b9fdfabfa3773f7a8ff75b71c60305a0676df0dc305ff443cf9376d0df144022c7067cce3c7469; __csrf=4ef64cd6787485a6cbd18a30ff78392f',
        'Host': 'music.163.com',
        'Upgrade-Insecure-Requests': '1',
        'Referer': "https://music.163.com",
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
    }

    proxies = {
        'http:': 'http://120.83.107.132:9999',
        'http:': 'http://163.204.240.23.197:9999'
    }
    response = requests.post(musicurl, headers=headers, proxies=proxies)
    print('获取评论请求url '+musicurl)
    if response.status_code == 200:
        data = json.loads(response.content)  # 将返回的值格式化为json
        if data['code'] != 200:
            print("被发现是爬虫 "+ song_name)
            exit(data['code'])
        else:
            return (data['total'])


def get_toal(music_id,song_name,driver):
    url = "https://music.163.com/#/song?id="+music_id
    driver.get(url)
    # 切换成frame
    driver.switch_to_frame("g_iframe")
    # 休眠3秒,等待加载完成!
    time.sleep(3)
    response = driver.page_source
    html = etree.HTML(response)
    comments = html.xpath("//span[@class='j-flag']/text()")

    if len(comments) > 0  and int(comments[0]) > 100000:
        print("获取 %s 的评论 %s 存储" % (song_name, comments[0]))
        return comments[0]
    else:
        print("获取 %s 的评论 %s 废弃" % (song_name, comments[0]))
        return None

# 将获得的歌手的热门歌曲id和名字写入csv文件
def write_to_csv(song_name,song_url,artist_name,driver):
    csvfile = open('./songs/hotsongs.csv', 'a', encoding='utf-8', newline='')  # 文件存储的位置
    writer = csv.writer(csvfile)
    #writer.writerow(('歌曲名称', '歌曲url','评论总数','歌手'))

    for name, url in zip(song_name, song_url):
        music_id = url.split('=')[-1]
        url = "https://music.163.com/#" + url
        try:
            if name is not None and url is not None:
                song_comments = get_total1(music_id,name)
                if  int(song_comments) > 100000:
                    print("获取 %s 的评论 %s 存储" % (name, song_comments))
                    writer.writerow([name, url, song_comments, artist_name])
                else:
                    print("获取 %s 的评论 %s 废弃" % (name, song_comments))

        except Exception as msg:
            print(msg)
            # 当程序的控制流程离开with语句块后, 文件将自动关闭


def main(driver):

    for item in read_csv():
        artist_name, artist_id = item
        # 可以任意选择浏览器,前提是要配置好相关环境,更多请参考selenium官方文档
        # 避免多次打开浏览器
        if artist_id != 'artist_id':
            url = "https://music.163.com/#/artist?id=" + str(artist_id)
            print("正在获取{}的热门歌曲...".format(artist_name))
            driver.get(url)
            # 切换成frame
            driver.switch_to.frame("g_iframe")
            # 休眠3秒,等待加载完成!
            time.sleep(2)
            response = driver.page_source

            html = etree.HTML(response)
            song_name = html.xpath("//span[@class='txt']/a/b/@title")
            song_url = html.xpath("//span[@class='txt']/a/@href")

            # 写入到csv文件里面
            write_to_csv(song_name, song_url,artist_name,driver)
            print("{}的热门歌曲写入到本地成功!".format(artist_name))


if __name__ == "__main__":
    driver = webdriver.Chrome(executable_path="/www/spider-music163/songs/chromedriver.exe")
    main(driver)
