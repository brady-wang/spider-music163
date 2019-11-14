from lxml import etree

from selenium import webdriver
import time
import csv


# 将获得的歌手的热门歌曲id和名字写入csv文件
def write_to_csv(song_name,song_url, artist_name):
    csvfile = open('./songs/hotsongs.csv', 'a', encoding='utf-8', newline='')  # 文件存储的位置
    writer = csv.writer(csvfile)
    writer.writerow(('歌曲名称', '歌曲url'))

    for name, url in zip(song_name, song_url):
        url = "https://music.163.com/#" + url
        try:
            if name is not None and url is not None:
                writer.writerow([name, url])
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


def main():
    driver = webdriver.Chrome()
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
            print("{}的热门歌曲获取完成!".format(artist_name))
            print("开始将{}的热门歌曲写入文件".format(artist_name))
            write_to_csv(song_name, song_url, artist_name)
            print("{}的热门歌曲写入到本地成功!".format(artist_name))


if __name__ == "__main__":

    main()
