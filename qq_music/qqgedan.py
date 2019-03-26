import os
import requests, json, re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def download_music(songmid, music_name, list_name):
    # url='https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?g_tk=872989112&jsonpCallback=MusicJsonCallback06459212607938936&loginUin=11297258&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8¬ice=0&platform=yqq&needNewCode=0&cid=205361747&callback=MusicJsonCallback06459212607938936&uin=11297258&songmid={0}&filename=C100{0}.m4a&guid=9136027940'.format(songmid)

    # https://u.y.qq.com/cgi-bin/musicu.fcg?callback=getplaysongvkey24583966914882927&g_tk=5381&jsonpCallback=getplaysongvkey24583966914882927&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&data={"req":{"module":"CDN.SrfCdnDispatchServer","method":"GetCdnDispatch","param":{"guid":"8809189374","calltype":0,"userip":""}},"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"8809189374","songmid":["002E3MtF0IAMMY"],"songtype":[0],"uin":"0","loginflag":1,"platform":"20"}},"comm":{"uin":0,"format":"json","ct":20,"cv":0}}
    data = json.dumps({"req": {"module": "CDN.SrfCdnDispatchServer", "method": "GetCdnDispatch",
                               "param": {"guid": "8334334694", "calltype": 0, "userip": ""}},
                       "req_0": {"module": "vkey.GetVkeyServer", "method": "CgiGetVkey",
                                 "param": {"guid": "8809189374", "songmid": [songmid], "songtype": [0], "uin": "0",
                                           "loginflag": 1, "platform": "20"}},
                       "comm": {"uin": 0, "format": "json", "ct": 20, "cv": 0}})
    url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?callback=getplaysongvkey32666490664609316&g_tk=5381&jsonpCallback=getplaysongvkey32666490664609316&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&data={}'.format(
        data)
    html = requests.get(url)
    # print(html.text)
    # 去掉jsonp
    music_json = json.loads(re.findall(r'^\w+\((.*)\)$', html.text)[0])
    print(music_json)
    base_url = music_json['req']['data']['freeflowsip'][0]
    filename = music_json['req_0']['data']['midurlinfo'][0]['filename']
    print('filename', filename)
    download_url = music_json['req_0']['data']['midurlinfo'][0]['purl']
    # 如果为空的话就是没有这首歌，QQ音乐没有版权
    if not download_url:
        return
    print('download_url1111', download_url)
    download_url = base_url + download_url
    print('download_url', download_url)

    # 下载到本地
    music = requests.get(download_url)
    print(music_name)
    print('music content =========== ', music.content)
    # print(music.content)
    # 判断歌单文件夹是否存在
    # 文件名去除特殊符号
    if not os.path.exists('F:/music/{}'.format(list_name)):
        os.mkdir('F:/music/{}'.format(list_name))
    with open("F:/music/{}/{}.m4a".format(list_name, re.sub(r'[\s+|@<>:\\"/]', '', music_name)), "wb") as m:
        m.write(music.content)


def view_html():
    # qq音乐页面是js加载的，这里用chrome headless模式访问
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome('F:/py/chromedriver', chrome_options=option)

    # 歌单页面，如果要换歌单请换歌单的url
    driver.get('https://y.qq.com/n/yqq/playsquare/1675523383.html')
    print(driver.title)
    try:
        # 等待播放列表链接便签加载完毕
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "songlist__song_txt")))
        list_name = driver.find_element_by_id('p_name_show').get_attribute('title')
        # lis= driver.find_elements_by_class_name('songlist__songname_txt')
        lis = driver.find_elements_by_xpath('//ul[@class="songlist__list"]/li//span[@class="songlist__songname_txt"]')
        print(len(lis))
        # 获取网页源代码，查看差别
        # html = driver.page_source
        # html = html.encode('utf-8')
        # with  open('test.html','wb') as f:
        #     f.write(html)
        pattern = re.compile(r'https://y.qq.com/n/yqq/song/(\S+).html')
        for i in range(lis.__len__()):
            li = lis[i]
            # a= WebDriverWait(driver, 20).until(lambda li: li.find_elements_by_class_name('js_song'))[i]
            a = li.find_element_by_class_name('js_song')
            # 获得songid
            href = a.get_attribute('href')
            # print(href)
            music_name = a.get_attribute('title')
            # print(music_name)
            m = pattern.match(href)
            # print(m)
            # print(m.group(1))
            download_music(m.group(1), music_name, list_name)

    finally:
        driver.quit()


if __name__ == '__main__':
    view_html()
