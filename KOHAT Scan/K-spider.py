# -*- coding: UTF-8 -*-
#页面爬行模块
import urllib,urllib2
import re,glob
import threading,Queue
import time
from multiprocessing import Pool
import os,sys
import os.path

'''0x01
获取页面下的任何url(可以用正则表达式匹配页面下的地址)
0x02
判断该url是否属于本域名下 并且判断是否已有爬取记录(还是用正则)
0x03
判断是否已经抓取

0x04
这里是对前几步的加以叙述 因为我们要进行批量扫描站点所以我们采用的方法是|多进程+多线程|
线程和进程的同步可能比较麻烦 但是可以试着用中间文件过渡 (但记得去掉重复的 这一步可以不做如果0x02做的好的话)  然后Scan重读取中间过渡文件 然后将获取到的内容提交到主动扫描模块
0x05
虽然这说的是页面爬行但也要知道 将不同的url分配到不同的主动扫描模块
例如页面中有 表格 后缀为.shtm ;.html ;.htm 应该提交到主动扫描的 sql injection
0x06
补充 在使用多线程的时候要记得用线程队列 Queue 
0x07
既然已经抓取到这些没有重复的Url了 那么下一步要做的就是分析Url 这里和0X05讲到的有所相似
但是我们不仅要判断页面的后缀并且要识别那些以PHP ASP ASPX JSP等结尾的页面是否要提交到XSS
或者要不要提交到SQL 还是XPATH等
0x08
既然我们都抓取到了这么多站点下的URL那么我要知道此URL是否是越权访问了某些我本身不能看的内容
我们可以捕获页面的标枪 匹配页面的关键内容 关键的是有关键词字典
0x09
0x10

'''
send_headers = {
 'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
 'Connection':'keep-alive'
}


def local_url_get():#获取本地BAIDU-URL SPIDER抓取到的搜索结果的Url
	path = os.path.abspath(sys.argv[0])#(获取本地地址)
	filelist = glob.glob(str(path)[:-11]+'scan report\*.md')
	local_file_list=[]
	for item in filelist:
		for each_one in(open(item,'r').readlines()):
			local_file_list.append(each_one.strip())
		try:
			os.remove(item)
		except:
			pass
	return local_file_list
	
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
		for each_all_page_url in all_page_url:
			try:
				if urllib2.urlopen(urllib2.Request(each_all_page_url,headers=send_headers)).code==200:
					URLlist.append(each_all_page_url)
			except Exception,e:
				pass
	return URLlist

def get_page_dom(URLlist):#判断页面内是否含有关键内容 关于越权访问之类的
	for eachurl in URLlist:


def find_Script_format(URLlist):#判断URL类型的sql 还有获取有forms的页面
	scriptlist=["?","php","asp","aspx","html","shtml","htm"]
