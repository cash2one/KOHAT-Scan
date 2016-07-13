# -*- coding: UTF-8 -*-
#页面爬行模块
import urllib,urllib2
import re,glob
import threading,Queue
import time
from multiprocessing import Pool
import os,sys
import os.path
import Queue
'''
详细叙述
关于站点spider自定义函数部件
一 获取本地baidu spider搜索结果
二 建立单独进程获取目标网站的页面(记得限定进程数不然电脑炸了 多进程好像可以不上锁 但我会在每个线程下建立多个线程进行获取这时候多线程就要上队列同步了)
三 既然站点页面都抓取了那么就要存放记录 放入result和information文件夹 应该每个站点爬行结果都新建个文件夹来存放以便记录
四 将获取的Url分配到各个子攻击模块(关于分配原则就后续加入)
五 此模块是用来判断页面是否为越权访问或者是信息泄露 但我觉得这应该是能一起判断的 我选择调用tester文件来检测
六 多线程或多线程 执行
七 filter
'''
send_headers = {
 'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20160101 Firefox/16.0',
 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
 'Connection':'keep-alive'
}


def local_url_get():#获取本地BAIDU-URL SPIDER抓取到的搜索结果的Url
#[a-zA-z]+://[^/]* 获取地址前部分 到.com .cn 之前的部分
	path = os.path.abspath(sys.argv[0])#(获取本地地址)
	filelist = glob.glob(str(path)[:-11]+'scan report\*.md')
	for item in filelist:
		try:
			files=open(item,'r').readlines()
			URLINEED=re.findall('[a-zA-z]+://[^/]*',files)
			os.remove(item)
		except:
			print 'local_url_get Eorro'
	return list(set(URLINEED))

def get_page_url(Url):#获取页面内的所有活的Url
	'''[a-zA-z]+://[^"]* 此正则可以匹配任何处于页面下的Url'''
	Req = urllib2.Request(Url)
	Page = urllib2.urlopen(Req,headers=send_headers)
	URLlist=[]
	if Page.code() == 200:
		'''开始获取页面下的url'''
		DOM=Page.raed()
		all_page_url = list(set(re.findall('[a-zA-z]+://[^"]*',DOM)))#顺便去掉重复的Url
		#判断是否匹配到非Url的东西
        for each_one in all_page_url:
            if urllib2.urlopen(urllib2.Request(each_one))==200:#除去一些非URL的元素
                URLlist.append(each_one)
        path = os.path.abspath(sys.argv[0])[:-11]
		for each_all_page_url in all_page_url:#将获取到的URL写入到result中
            try:
                if os.path.exists(str(path+each_all_page_url))==True:
                    pass
                else:
                    os.mkdir(str(path)+'\scan report'+'\\'+str(each_all_page_url))
                files=open(str(path+"\scan report"+'\\'+each_all_page_url)+str('\Url report.md'),'w+')
                for URLX in URLlist:
                    files.writelines(str(URLX)+'\n')
                files.close()
            except Exception,e:
                print 'Eorro',e

        return URLlist


def find_Script_type(URLlist):#判断URL类型 决定sql 注入方式 
	scriptlist=[".php",".asp",".aspx",".html",".shtml",".htm"]
	phplist=[]
	asplist=[]
	aspxlist=[]
	htmllist=[]
	shtmllist=[]
	htmlist=[]
	for formsURL in URLlist:#判断脚本类型 不同的脚本对于的查询方式有差别 比如伪静态是*****.htm 动态是?=****  我星号就代替语句啦:)
		if formsURL.find('.php')==True:
			phplist.append(formsURL)
		else:
			pass
		if formsURL.find('.asp')==True:
			asplist.append(formsURL)
		else:
			pass
		if formsURL.find('.aspx')==True:
			aspxlist.append(formsURL)
		else:
			pass
		if formsURL.find('.html')==True:
			htmllist.append(formsURL)
		else:
			pass
		if formsURL.find('shtml')==True:
			shtmllist.append(formsURL)
		else:
			pass
		if formsURL.find('htm')==True:
			htmlist.append(formsURL)
		else:
			pass
	return phplist,asplist,aspxlist,htmllist,shtmllist,htmlist

def find_the_forms(URLlist):#获取html中的表单 根据html的form来跟踪表达
'''    url = "http://xxxxxx/opac_two/search2/searchout.jsp"
    search = urllib.urlencode( [('suchen_type', '1'), ('suchen_word', a.encode('gb18030')),
            ('suchen_match', 'qx'), ('recordtype', 'all'), ('library_id', 'all'),('show_type','wenzi')])
        req = urllib2.Request(url)
        fd = urllib2.urlopen(req, search).read()
        html = fd.decode('gb18030').encode('utf-8')   这个有点麻烦 我就先写threadingpool'''


	for each_url in URLlist:
		dom = urllib2.urlopen(urllib2.Request(each_url))
		re_forms = re.findall(dom,'')

		post_form = urllib2.urlopen(urllib2.Request(),)



#将每一个站点的搜索分给线程 所以要将local_url_get()的内容传递给 多进程让多进程再将任务具体到多线程 提高效率
def threadingpool(URLlist):#队列锁 记得上 多线程一定要不然会写入错误  多进程可以不用
    Q = Queue.Queue(250)
    
    for i in :
        t=threading.Thread(target = get_page_url, args = (URLlist), name = 'spider' + str(i))
        t.start()



def multiprocessingpool(URLlist):




if __name__ == '__main__':
    keywordlist=[]
    URLlist=get_page_url()