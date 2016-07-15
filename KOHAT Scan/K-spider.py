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



send_headers = {
 'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20160101 Firefox/16.0',
 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
 'Connection':'keep-alive'
}
q=Queue.Queue()
result=list()
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

def get_page_url(Url,Nones):#获取页面内的所有活的Url
	'''[a-zA-z]+://[^"]* 此正则可以匹配任何处于页面下的Url'''
	Req = urllib2.Request(Url,headers=send_headers)
	Page = urllib2.urlopen(Req)
	all_page_url=[]
	URLlist=[]
	fliters=[]
	try:
		if str(Page.code) == '200':
			'''开始获取页面下的url'''
			DOM = Page.read()
			all_page_url = list(set(re.findall('[a-zA-z]+://[^"]*',DOM)))#顺便去掉重复的Url
            #如果大列表中已经有小列表的url那么 就跳过 没就加入
			for all_url in all_page_url:
				if len(result)>0:
					for each_url in result:
						if each_url==all_url:
							all_page_url.remove(all_url)
		else:
			time.sleep(2)
			pass
	except Exception,e:
		print 'a'
    #去掉脚本连接 .css .js
    #while  True:
    	for script_url in all_page_url:
    		if script_url.find('.js')>0 or script_url.find('.css')>0:
    			all_page_url.remove(script_url)
    	for a in all_page_url:
    		try:
    			for fliter in a.split("'"):
    				if not re.match('[a-zA-z]+://[^"]*',a)==None:
    					all_page_url.remove(a)
    					fliters.append(fliter)
    				else:
    					all_page_url.remove(a)
    		except:
    			pass
        for x in fliters:
        	q.put(x)
        return fliters



def find_Script_type(URLlist):#判断URL类型 决定sql 注入方式
	scriptlist=[".php",".asp",".aspx",".html",".shtml",".htm"]
	phplist=[]
	asplist=[]
	aspxlist=[]
	htmllist=[]
	shtmllist=[]
	htmlist=[]
	for formsURL in URLlist:#判断脚本类型 不同的脚本对于的查询方式有差别 比如伪静态是*****.htm 动态是?=****  我星号就代替语句啦:)
		if formsURL.find('.php')>0:
			phplist.append(formsURL)
		else:
			pass
		if formsURL.find('.asp')>0:
			asplist.append(formsURL)
		else:
			pass
		if formsURL.find('.aspx')>0:
			aspxlist.append(formsURL)
		else:
			pass
		if formsURL.find('.html')>0:
			htmllist.append(formsURL)
		else:
			pass
		if formsURL.find('shtml')>0:
			shtmllist.append(formsURL)
		else:
			pass
		if formsURL.find('htm')>0:
			htmlist.append(formsURL)
		else:
			pass
	return phplist,asplist,aspxlist,htmllist,shtmllist,htmlist

def find_the_forms(URLlist):#获取html中的表单 根据html的form来跟踪表达
    '''url = "http://xxxxxx/opac_two/search2/searchout.jsp"
    search = urllib.urlencode( [('suchen_type', '1'), ('suchen_word', a.encode('gb18030')),
            ('suchen_match', 'qx'), ('recordtype', 'all'), ('library_id', 'all'),('show_type','wenzi')])
        req = urllib2.Request(url)
        fd = urllib2.urlopen(req, search).read()
        html = fd.decode('gb18030').encode('utf-8')'''
    for each_url in URLlist:
		dom = urllib2.urlopen(urllib2.Request(each_url))
		re_forms = re.findall(dom,'')

		post_form = urllib2.urlopen(urllib2.Request(),)



#将每一个站点的搜索分给线程 所以要将local_url_get()的内容传递给 多进程让多进程再将任务具体到多线程 提高效率
#开队列 将线程放入队列 判断队列有没有超量 有就等 没就加进去
def  threadingpoools(into_url):
	first_url_list=into_url
	thread=[threading.Thread(target=get_page_url,args=(urls,None)) for urls in first_url_list]
	for t in thread:
		t.start()
	while not q.empty():
		global result
		result.append(q.get())
	return result
#既然有队列同步URL了 那么我们可以判断队列中是否有一样的url从而发现是不是爬取了相同的URL

def multiprocessingpool(URLlist):
	pool = Pool(20)
	for i in URLlist:
		result.append(pool.apply(threadingpoools,URLlist))
		pool.close()
		pool.join()
		return result

def result_writein(info):
    all_page_url=info
    path = unicode(os.path.abspath(sys.argv[0])[:-11],'cp936')
    for each_all_page_url in all_page_url:
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

if __name__ == '__main__':
    threadingpoools([u'http://www.baidu.com',u'https://atom.io/'])
