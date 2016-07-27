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
Q=Queue.Queue()
def local_url_get():#获取本地BAIDU-URL SPIDER抓取到的搜索结果的Url
#[a-zA-z]+://[^/]* 获取地址前部分 到.com .cn 之前的部分
	path = os.path.abspath(sys.argv[0])#(获取本地地址)
	filelist = glob.glob(str(path)[:-11]+r'scan report\*.md')
	Biglist=[]
	for item in filelist:
		try:
			files=open(item,'r').readlines()
			for filesz in files:
				URLINEED=re.findall('[a-zA-z]+://[^/]*',filesz)
				for plan in URLINEED:
					Biglist.append(plan)
			os.remove(item)
		except Exception,e:
			print 'Eorro,file not exists! and',e
	URLlist=list(set(Biglist))
	return URLlist



def get_page_url(Url,Nones):#获取页面内的所有活的Url
	'''[a-zA-z]+://[^"]* 此正则可以匹配任何处于页面下的Url'''
	fliters=[]
	fliter1=[]
	try:
		Req = urllib2.Request(Url,headers=send_headers)
		Page = urllib2.urlopen(Req,timeout=15)
	except Exception,e:#被服务端重置[Errno 10054]或自身网络问题错误[<urlopen error [Errno 11001] getaddrinfo failed>] 等待1秒后继续获取
		time.sleep(2)
		try:
			Req = urllib2.Request(Url,headers=send_headers)
			Page = urllib2.urlopen(Req,timeout=15)
		except:
			pass

	domain=re.match('[a-zA-z]+://[^/]*',Url).group(0)
	all_page_url=[] 
	try:
		if Page.code==200:
			'''开始获取页面下的url'''
			DOM = Page.read()
			all_page_url = list(set(re.findall(r'\b'+domain+r'\b'+r'[^"]*',DOM)))#顺便去掉重复的Url
            #如果大列表中已经有小列表的url那么 就跳过 没就加入
	except Exception,e:
		pass
    #去掉脚本连接 .css .js .jgp .png
    	for script_url in all_page_url:
    		if script_url.find('.js')>0 or script_url.find('.css')>0 or script_url.find('.jpg')>0 or script_url.find('.png')>0:
    			pass
    		else:
    			fliter1.append(script_url)
    	
    	#情况二 页面是用 /xxxx/xxx.html之类的来打开站点下的页面 这样上面就无效了
    	try:
    		if len(re.findall("[']+/[^']*",DOM))>=len(re.findall('["]+/[^"]*',DOM)):
    			domurl = re.findall("[']+/[^']*",DOM)
    		else:
    			domurl = re.findall('["]+/[^"]*',DOM)
    	except Exception, e:
    		pass

    	try:
    		if  len(re.findall("[']+/[^']*",DOM))>=len(re.findall('["]+/[^"]*',DOM)):
    			for url_d in domurl:
    				all_page_url.append(domain+url_d.strip("'"))
    		else:
    			for url_d in domurl:
    				all_page_url.append(domain+url_d.strip('"'))
    	except Exception, e:
    		pass


    	try:
    		for e in range(len(all_page_url)):
    			if all_page_url[e].find("google.com")>0 or all_page_url[e].find(".js")>0 or all_page_url[e].find(".png")>0 or all_page_url[e].find(".jpg")>0 or all_page_url[e].find(".css")>0 or all_page_url[e].find('.xml')>0:
    				pass
    			else:
    				fliter1.append(all_page_url[e])
    	except Exception, e:
    		pass
    	
#url后可能接的是'  > ;所以要切 几次至于"因为我正则匹配到双引号为止所以不会出现 　晚上写上这段
        plist=['<','>',';',"'"]
        for i in fliter1:
        	if not re.match('[a-zA-z]+://[^"]*',i)==None and not len(re.findall(r"[<>;']",i))>0:
        		fliters.append(i)
        	else:
        		for e in i.split("'"):
        			if not re.match('[a-zA-z]+://[^"]*',e)==None:
        				for f in e.split(">"):
        					if not re.match('[a-zA-z]+://[^"]*',f)==None:
        						for g in f.split(";"):
        							if not re.match('[a-zA-z]+://[^"]*',g)==None:
        								for h in g.split("<"):
        									if not re.match('[a-zA-z]+://[^"]*',h)==None:
        										fliters.append(h)
        										
    	try:
    		for h in list(set(fliters)):
    			Q.put(h)
        except Exception, e:
    		print e,'q.put() fault'
    	try:
    		for x in list(set(fliters)):
    			q.put(x)
        except Exception, e:
    		print e,'q.put() fault'


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



def  threadingpoools(into_url):
	first_url_list=into_url
	if len(first_url_list)>0:
		thread=[threading.Thread(target=get_page_url,args=(urls,'Thread-1')) for urls in first_url_list]
		for t in thread:
			t.start()
	else:
		pass


def multiprocessingpool(URLlist):
	pool = Pool(20)
	for i in URLlist:
		result.append(pool.apply(threadingpoools,URLlist))
		pool.close()
		pool.join()	



def result_writein(info):#感觉应该在全部完成后再调用
    all_page_url=sorted(list(set(info)))
    path = os.path.abspath(sys.argv[0])[:-11]
    netstation=[re.match(r'[a-zA-z]+://[^//]*',x).group(0) for x in all_page_url]
    for ww in netstation:
    	if os.path.exists(str(path)+r'emp'+'\\'+ww.replace(r'://','~'))==True:#看文件夹是否存在
    		os.mkdir(str(path)+r'temp'+'\\'+ww.replace(r'://','~'))#不在创建文件夹
    		pass
    	else:
    		ff=open(str(path)+r'temp'+'\\'+ww.replace(r'://','~')+ww.replace(r'://','~')+r'.md','w+')#有就在里面创建文件夹
    		ff.close()
    for each_all_page_url in all_page_url:
    	for ww in netstation: 
    		if ww==re.match(r'[a-zA-z]+://[^//]*',each_all_page_url).group(0):
				filess=open(str(path+r"temp"+'\\'+each_all_page_url)+str('\Url report.md'),'a')
				filess.writelines(str(URLX)+'\n')
				filess.close()



def run(domainurl):
	result2=[]
	differences=[]
	origin = list(set(threading.enumerate()))
	threadingpoools(domainurl)
	time.sleep(2)
	#所有线程都完成后也要等q和Q空了后才能退出 这意味着要3个都是false才能退出 有一个true就得进行
	while  not q.empty() or not Q.empty():#not list(set(threading.enumerate()))==origin or
		time.sleep(0.2)
		differences.append(Q.get())
		if not len(list(set(differences).difference(set(result2))))==0:
			different=list(set(differences).difference(set(result2)))
			threadingpoools(different)
			print different
		else:
			pass
		result2.append(q.get())
	print 'finished:',result2
	'''script_urls=list(set(find_Script_type(result2)))#找脚本类型'''
	'''formslist=list(set(find_the_forms(result2)))#看有没有表单'''

def read_conf():
	pass


if __name__ == '__main__':
	for task in local_url_get():
		multiprocessingpool(run(i))
