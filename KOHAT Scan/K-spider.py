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
    			fliters.append(script_url)
    	for a in all_page_url:
    		try:
    			for fliter in a.split("'"):
    				if not re.match('[a-zA-z]+://[^"]*',a)==None:
    					#看出错误匹配的 那些连标枪也匹配进来的 一般是以'为结尾的会匹配错误所以 从'来切开每一个错误匹配内容
    					#在从中遍历每一个元素 看那些元素是Url 但是无论如何都是要把元素删了再加 测试完毕OK没事 小心列表长度缺失会有个很麻烦的问题 所以还是有减有加保持长度好
    					fliters.remove(a)
    					fliters.append(fliter)
    				else:
    					fliters.remove(a)
    		except:
    			pass
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

    	print list(set(all_page_url))


    	try:
    		for e in range(len(all_page_url)):
    			if all_page_url[e].find("google.com")>0 or all_page_url[e].find(".js")>0 or all_page_url[e].find(".png")>0 or all_page_url[e].find(".jpg")>0 or all_page_url[e].find(".css")>0 or all_page_url[e].find('.xml')>0:
    				pass
    			else:
    				fliters.append(all_page_url[e])
    	except Exception, e:
    		pass
        print list(set(fliters))

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
        return list(set(fliters))


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
	thread=[threading.Thread(target=get_page_url,args=(urls,None)) for urls in first_url_list]
	for t in thread:
		t.start()
#差集并集算法爬行即可



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
	threadingpoools(list(domainurl))
	time.sleep(2)
	#所有线程都完成后也要等q和Q空了后才能退出 这意味着要3个都是false才能退出 有一个true就得进行
	while not list(set(threading.enumerate()))==origin or not q.empty() or not Q.empty():
		differences.append(Q.get())
		different=list(set(differences).difference(set(result2)))
		threadingpoools(different)
		result2.append(q.get())
		print list(set(result2)),list(set(threading.enumerate())),origin
	print result2
	'''script_urls=list(set(find_Script_type(result2)))#找脚本类型'''
	'''formslist=list(set(find_the_forms(result2)))#看有没有表单'''



if __name__ == '__main__':
	for task in local_url_get():
		multiprocessingpool(run(i))
	#站点列表→每个进程→多线程→线程重复爬行→站点爬行完毕→再查看页面中脚本类型与本站含有表单的页面 
	#脚本类型的查询还是 在sql injection 写吧 这留着做个参考
	#get_page_url 需要加个判断Url是否是本站下的 不然会跨站爬虫了
	#文件写入应该写入到temp文件夹 

	#爬虫 访问页面获取URL 得知URL与大集合result的差集 访问差集再次获取Url 再次求差集 访问差集的Url 
	#我们在page_url_get中已经要求差集 然后将得到的差集global 分配到run中然后再分配 run中分配完一个url就删一个url直到差集小于一个值
	#2016年7月17日 22:35:56 为写入重新连接代码  电脑会出现短暂"断网"所以我们要写一个timeout=3