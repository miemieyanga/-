import urllib.request
from get_url import get_html,get_all
import re
import time
import random

def get_name(html):
    s = re.search(r"<span property=\"v:itemreviewed\">.*</span>",html).group()
    name = s[32:-7]
    return name

def get_info(html):
    name = get_name(html)
    s = re.search(r"<strong class=\"ll rating_num\" property=\"v:average\">.*</strong>",html).group()
    rating_num = s[-12:-9]
    return name +' '+ rating_num

def get_data(url):
    starList = ["很差", "较差", "还行", "推荐", "力荐"]

    for i in range(0,201,20):
        cur_url = url + 'comments?start='+str(i)+'&limit=20&sort=new_score&status=P'
        html = get_html(cur_url)

        cur_f = html.find('<div class=\"comment-item\"')
        while cur_f != -1:
            cur_p = html.find('<div class=\"comment-item\"', cur_f + 20)
            if cur_p != -1:
                temp = html[cur_f:cur_p]
                get_people(temp)

            else:
                temp = html[cur_f:]
                get_people(temp)

            cur_f = html.find('<div class=\"comment-item\"',cur_p)

def get_people(html):
    s = re.search(r"<a href=\"https://www.douban.com/people/.*/\".*>.*</a>",html).group()
    link = re.search(r"https://www.douban.com/people/.*/",s[:-5]).group(0)
    id = re.search(r">.*</a>",s).group(0)[1:-4]
    with open("test.txt","a",encoding='utf-8') as f:
        f.write(link+'   '+id+"\n")


if __name__ == "__main__":
    with open("url.txt","r") as f:
        urlList = f.readlines()
        for url in urlList:
            url = url[:-1]

        # html = get_html(url)
            get_data(url)
        # print(get_info(html))
