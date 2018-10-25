import requests
import json
import re
import random
import time

def get_one_page(url):
    # ipList = ['183.230.177.118','123.235.32.36','121.196.196.93','114.234.80.196']
    # cur_ip = random.randchoice(ipList)
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    response = requests.get(url,headers = headers)
    if response.status_code != 200:
        print('request error')
        print(response.status_code)
        return None
    response.encoding = "utf-8"
    return response.text

def find_comment(s):
    # id
    id = ""
    target = re.search(r"<a href=\"https://www.douban.com/people/.*>.*<",s).span()
    stop = False
    i = 2
    while not stop:
        if s[target[1]-i] == ">":
            stop = True
        else:
            id = s[target[1]-i] + id
            i = i + 1

    # star
    starList = ["很差","较差","还行","推荐","力荐"]
    try:
        keysentence = re.search(r"<span class=\"allstar.*></span>",s).group(0)
        keyword = keysentence[-11:-9]
        star = starList.index(keyword)+1
    except:
        star = 1.5

    # comment
    comment = ""
    start = s.find("<span class=\"short\">")
    end = s.find("</span>",start + 20)
    comment = s[start+20:end]
    return 'id = ' + id  + "      star = " + str(star) +"\n\n" + comment + "\n\n\n"

def get_comment(html_comment):
    cur_comments = []
    cur_f = html_comment.find('<div class=\"comment-item\"')
    while cur_f != -1:
        cur_p = html_comment.find('<div class=\"comment-item\"',cur_f+20)
        if cur_p != -1:
            temp = html_comment[cur_f:cur_p]
            cur_comments.append(find_comment(temp))
            cur_f = cur_p
        else:
            break

    return cur_comments

if __name__ == '__main__':
    init_url = r"https://movie.douban.com/subject/24852545/comments?start=0&limit=20&sort=new_score&status=P"
    number = 0
    page = 1
    for i in range(0,20):
        
        n = i*20
        start = n
        url = r"https://movie.douban.com/subject/24852545/comments?start="+str(start)+r"&limit=20&sort=new_score&status=P"
        
        html = get_one_page(url)
        
        start = html.find('<div class=\"mod-bd\" id=\"comments\">')
        end = html.find('<div class=\"comments-footer-tips\">')
        comments = get_comment(html[start:end])

        print("current-page: "+str(page))
        page = page + 1
        for i in range(len(comments)):
            try:
                print(str(number) + comments[i])
                number = number + 1
            except:
                pass
        t = random.randint(50,200)
        # time.sleep(t//5)
    print("总条数："+str(number))
    #with open('hhh.txt','w') as f:
        #f.write(get_one_page(url))
