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

        print('sleep......')
        time.sleep(60)

def get_place(url):
    print(url)
    html = get_html(url)
    find = False

    try:
        start = re.search("常居",html).span()[0]
        find = True
        html = html[start:start+1000]
    except Exception as e:
        place = e

    if find:
        s2 = re.search(r"\">.*</a>",html).group()
        place = s2[2:-4]

    print(place)
    return place

def get_people(html):
    starList = ["很差", "较差", "还行", "推荐", "力荐"]

    s = re.search(r"<a href=\"https://www.douban.com/people/.*/\".*>.*</a>",html).group()
    link = re.search(r"https://www.douban.com/people/.*/\"",s[:-5]).group(0)[:-2]
    id = re.search(r">.*</a>",s).group(0)[1:-4]
    try:
        s2 = re.search(r"<span class=\"allstar[0-9]* rating\" title=\".*\"></span>",html).group(0)
        star = re.search(r"title=\".*\"",s2).group(0)[7:9]
        mark = starList.index(star) + 1
    except:
        mark = -1

    place = get_place(link)
    # time.sleep(random.randint(10,50)/5)
    if mark != -1:
        if place != "hh":
            if mark == 5:
                with open("mark5.txt","a",encoding='utf-8') as f:
                    f.write("id:%-30s place:%-20s\n"%(id,place))
            elif mark == 4:
                with open("mark4.txt","a",encoding='utf-8') as f:
                    f.write("id:%-30s place:%-20s\n"%(id,place))
            elif mark == 3:
                with open("mark3.txt","a",encoding='utf-8') as f:
                    f.write("id:%-30s place:%-20s\n"%(id,place))
            elif mark == 2:
                with open("mark2.txt","a",encoding='utf-8') as f:
                    f.write("id:%-30s place:%-20s\n"%(id,place))
            else:
                with open("mark1.txt","a",encoding='utf-8') as f:
                    f.write("id:%-30s place:%-20s\n"%(id,place))
    """
    with open("test.txt","a",encoding='utf-8') as f:
        if mark != -1:
            if place != "hh":
                f.write(str(mark)+'   '+id+"      "+place+"\n")
    """

if __name__ == "__main__":
    with open("url.txt","r") as f:
        urlList = f.readlines()
        for url in urlList:
            url = url[:-1]

        # html = get_html(url)
            get_data(url)
        # print(get_info(html))
