# -学着写爬虫
豆瓣评论爬取十页之后要求登陆，登陆之后还要输入验证码，难受啊马飞--
这样可以改变思路，爬取上百个电影的前十页评论

get_url用来得到250个影评界面的url
请求次数太多，导致403
解决方法：先请求得到url保存，然后对每一个url分别爬取
