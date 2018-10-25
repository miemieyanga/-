import urllib.request
import re
import time


def get_html(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299')
    html = urllib.request.urlopen(req)
    html = html.read().decode('utf-8')
    return html


def get_url(html, urlList):
    temp = re.findall(r"<a href=\"https://movie.douban.com/subject/[0-9]*/\" class=\"\">", html)
    for item in temp:
        urlOfFilm = re.search(r"https://movie.douban.com/subject/[0-9]*/", item).group()
        urlList.append(urlOfFilm)


def get_all():
    urlList = []
    html = get_html('https://movie.douban.com/top250')
    get_url(html, urlList)
    for i in range(25, 250, 25):
        time.sleep(1)
        html = get_html('https://movie.douban.com/top250?start=' + str(i) + '&filter=')
        get_url(html, urlList)

    return urlList

    # for item in urlList:
    #    print(item)


if __name__ == "__main__":
    get_all()
