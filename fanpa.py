# encoding: utf-8
"""
Author: tn
CreateTime: 2022-3-15
UpdateTime: 2022-3-15
Info:  爬取并处理国家卫健委每日疫情防控数据，截至3月14日24时新型冠状病毒肺炎疫情最新情况
        反爬
"""


import os
import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup
from pyppeteer import launcher

# 在导入 launch 之前 把 --enable-automation 禁用 防止监测webdriver
launcher.DEFAULT_ARGS.remove("--enable-automation")

from pyppeteer import launch


def saveFile(path, filename, content):
    if not os.path.exists(path):
        os.makedirs(path)

    # 保存文件
    with open(path + filename + ".txt", 'w', encoding='utf-8') as f:
        f.write(content)

def getContent(html):
    bsobj = BeautifulSoup(html, 'html.parser')
    cnt = bsobj.find('div', attrs={"id": "xw_box"}).find_all("p")
    s = ""

    #
    if cnt:
        for item in cnt:
            s += item.text
        return s

    return "爬取失败！"

def getTitleUrl(html):
    bsobj = BeautifulSoup(html, 'html.parser')
    titleList = bsobj.find('div', attrs={"class": "list"}).ul.find_all("li")
    for item in titleList:
        link = "http://www.nhc.gov.cn" + item.a["href"];
        title = item.a["title"]
        date = item.span.text
        yield title, link, date

def getListUrl(html):
    bsobj = BeautifulSoup(html, 'html.parser')
    titleList = bsobj.find('div', attrs={"class": "list"}).ul.find_all("li")
    for item in titleList:
        link = "http://www.nhc.gov.cn" + item.a["href"];
        title = item.a["title"]
        date = item.span.text
        yield title, link, date

def getPageUrl():
    for page in range(1,7):
        if page == 1:
            yield 'http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml'
        else:
            url = 'http://www.nhc.gov.cn/xcs/yqtb/list_gzbd_'+ str(page) +'.shtml'
            yield url

async def pyppteer_fetchUrl(url):
    browser = await launch({'headless': False, 'dumpio': True, 'autoClose': True})
    page = await browser.newPage()

    await page.goto(url)
    await asyncio.wait([page.waitForNavigation()])
    str = await page.content()
    await browser.close()
    return str


def fetchUrl(url):
    return asyncio.get_event_loop().run_until_complete(pyppteer_fetchUrl(url))

if "__main__" == __name__:



    for url in getPageUrl():
        s = fetchUrl(url)
        for title, link, date in getTitleUrl(s):
            print(title, link)
            # 如果日期在1月21日之前，则直接退出
            mon = int(date.split("-")[1])
            day = int(date.split("-")[2])
            if mon == 3 and day == 14:
                html = fetchUrl(link)
                content = getContent(html)
                print(content)
                # saveFile("D:/Python/NHC_Data/", title, content)
                print("-----" * 20)
