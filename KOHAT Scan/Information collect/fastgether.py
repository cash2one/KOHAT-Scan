import urllib2
import re
import time
import sys
import os
import threading
import Queue
import getopt
import random
from multiprocessing.dummy import Pool

#write by kcorlidy  it uses to gether top board;information of website(domains,the weight) 

send_headers = [{
 'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:49.0) Gecko/20100101 Firefox/49.0',
 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
 'Connection':'keep-alive'
}
,
 {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
 'Accept':'*/*',
 'Connection':'keep-alive'
},
{'User-Agent':"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.154 Safari/537.36 LBBROWSER",
 'Accept':'*/*',
 'Connection':'keep-alive'
}]

li=['http://top.chinaz.com/hangye/index_yule.html','http://top.chinaz.com/hangye/index_shopping.html',
	'http://top.chinaz.com/hangye/index_gov.html','http://top.chinaz.com/hangye/index_jiaoyu.html',
	'http://top.chinaz.com/hangye/index_qiye.html','http://top.chinaz.com/hangye/index_shenghuo.html',
	'http://top.chinaz.com/hangye/index_wangluo.html','http://top.chinaz.com/hangye/index_tiyu.html',
	'http://top.chinaz.com/hangye/index_yiliao.html','http://top.chinaz.com/hangye/index_jiaotonglvyou.html',
	'http://top.chinaz.com/hangye/index_news.html']

Q=Queue.Queue()
max_basetime=4
#gether all kind of toplist 
def gather_the_top_type_in_the_kind():
	global dictQ
	dictQ=[]
	for i in li:
		Req = urllib2.Request(i,headers=send_headers)
		Page = urllib2.urlopen(Req,timeout=15)
		DOM=Page.read()
		rex=re.findall(r'"'+i[29:-5]+r'[^]*[^<]*',DOM)
		for x in rex:
			try:
				if not x.find('zonghe')>0 and not len(re.findall(r'_\d[^.]*',x))>0 and not x.find('pr.html')>0 and not x.find('br.html')>0 and not x.find('class="tagCurt"')>0 and not x.find('alexa.html')>0 and not x.find('>1')>0:
					dictQ.append(x.split('">'))
			except:
				pass
		time.sleep(3)
	xfile=open('toplist_type'+ str(time.ctime().replace(":","_"))+'.md','w+')
	for xfiles in dictQ:
		xfile.write(xfiles[0][1:]+"  "+xfiles[1]+'\n')
	xfile.close()

#gather toplist  mention: one input and it should be str,or it may be blockaded by security stactics
#col-gray[^]*[^<():]*  gather website and it have suitable queue to us to order their sequence; [1:] is what we need
#http://rank.chinaz.com/?host=
def gather_what_kind_of_toplist_you_wander(info_toplist):
	info_top=info_toplist
	info_toplist_page=[info_top[:-5]+"_"+str(i)+".html" for i in range(2,3)]# EACH PAGE
	info_toplist_page.append(str(info_toplist))
	information_searcher=[]
	if 1:
		for x in info_toplist_page:
			Reqs = urllib2.Request(x,headers=send_headers)
			Pages = urllib2.urlopen(Reqs,timeout=15)
			DOMs=Pages.read()
			re_urls=re.findall(r"col-gray[^]*[^<():]*",DOMs)[1:]
			re_urls_fliter=[str(each[10:]) for each in re_urls]
			print re_urls_fliter




#it coulid help you gather witch website information that you wander,list or string only, if you input list this will gather all you input
#i would judge if your input_type
#i dont know how to judge  path or url
def gather_each_Urls_informatin(info_website):
	#for each Urls info and gather information
	print info_website
	if 1:
			if 1:
				base_time=2
				re_information_Subdomain=[]
				re_information_weight=[]
				re_website_IP_address=[]
				re_website_physical_address=[]
				re_under_same_IP_adress=[]
				DOMx=""
				DOMY=""
				DOMZ=""
				try:
					Reqx = urllib2.Request("http://rank.chinaz.com/?host="+str(info_website),headers=send_headers[int(random.randint(0,2))])
					Pagex = urllib2.urlopen(Reqx,timeout=15)
					DOMx=Pagex.read()
				except Exception,e:
					if e=="<urlopen error [Errno 10060] >":
							time.sleep(base_time)
							if base_time<max_basetime:
								base_time+=1

				#website weight and Subdomain
				re_information_Subdomain=[ismd[8:] for ismd in re.findall(r"qq.com.{2}[^<]*",DOMx) if ismd[8:].find(info_website)>=0] # it is domains !
				re_information_weight=[weight[0:weight.find("<")-1]+" "+weight[weight.find('>')+1:] for weight in re.findall(r"\w*.<i id[^]*[<]*",DOMx)] #it is weight !
				
				#website IP adress,physical_address
				while len(DOMY)<5000:
					try:
						time.sleep(1)
						ReqY = urllib2.Request("http://ip.chinaz.com/?ip="+str(info_website),headers=send_headers[int(random.randint(0,2))])
						PageY = urllib2.urlopen(ReqY,timeout=15)
						DOMY=PageY.read()
					except Exception,e:
						print "Part Y error:",e
						if str(e)=="<urlopen error [Errno 10060] >":
							continue
							time.sleep(base_time)
							if base_time<max_basetime:
								base_time+=1

				re_website_IP_address=[ip[24:] for ip in re.findall(r"class=.Whwtdhalf w15-0.[^]*[<]*",DOMY)[2:] if ip.find(".")>0 and not ip.find(info_website)>0] #get ip adress 
				re_website_physical_address=[phy[7:] for phy in re.findall(r'w50-0.{2}[^]*[<]*',DOMY)] #physical_address
				
				#which website under the same IP adress
				while len(DOMZ)<3000:
					try:
						time.sleep(1)
						ReqZ = urllib2.Request("http://s.tool.chinaz.com/same?s="+str(info_website)+"&page=1",headers=send_headers[int(random.randint(0,2))])
						PageZ = urllib2.urlopen(ReqZ,timeout=20)
						DOMZ=PageZ.read()
					except Exception,e:
						print "Part Z error:",e
						if base_time<max_basetime:
								base_time+=1
						if str(e)=="<urlopen error [Errno 10060] >":
							continue
							time.sleep(base_time)
					
				re_under_same_IP_adress=[Z[18:] for Z in re.findall(r"overhid.{3}a href.{2}[^]*[^']*",DOMZ)]

				
				print len(re_information_weight)
				print len(re_website_IP_address)
				print len(re_website_physical_address)
				print len(re_information_Subdomain)
				print len(re_under_same_IP_adress)
				print len(DOMZ),len(DOMY),len(DOMx)
				#print len(DOMZ),len(DOMY)
				#print len(re.findall(r"overhid.{3}a href.{2}[^]*[^']*",DOMZ))

				weight_name=['baidu weight','keywords','IP flow']
				result_files=open(str(info_website)+" "+str(time.ctime().replace(":","_"))+'.md','w+')

				result_files.write("information weight"+"\n")
				for weights in range(len(re_information_weight)-1):	
					result_files.write(weight_name[weights]+":"+re_information_weight[weights]+"\n")

				result_files.write("\n"*3+"website IP adress and its physical address"+"\n")
				for ip_adress in range(len(re_website_physical_address)-1):
					result_files.write(re_website_IP_address[ip_adress]+"  "+re_website_physical_address[ip_adress+1]+"\n")

				result_files.write("\n"*3+"its Subdomains"+"\n")
				for Subdomains in range(len(re_information_Subdomain)):
					result_files.write(re_information_Subdomain[Subdomains]+"\n")

				result_files.write("\n"*3+"what else website under the IP adress[target website ip adress]"+"\n"+"http://s.tool.chinaz.com/same?s="+str(info_website)+"&page=1"+"\n")
				for same_IP in re_under_same_IP_adress:
					result_files.write(same_IP+"\n")
				result_files.close()




def auto_function(info):
	try:
		opts, args = getopt.getopt(info,"hu:p:t:",["toplist=","path=","url="])
	except getopt.GetoptError:
		print 'fastgether.py -t <toplist Url>, -p <file path> , -u <target Url>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'fastgether.py -t <toplist Url>, -p <file path> , -u <target Url>'
			sys.exit()
		elif opt in ("-t", "--toplist"):
			outfo = arg
			gather_what_kind_of_toplist_you_wander(outfo)
		elif opt in ("-p", "--path"):
			outfo = arg
			try:
				filex=open(info,'r+')
				info_page=[lists.strip() for lists in filex.readlines()]
				filex.close()
				processing_Dummy(info_page)
			except Exception,e:
				print (e)
		elif opt in ("-u", "--url"):
			outfo = arg
			if outfo.find("http")>=0 and outfo.find("www")>=0:
				gather_each_Urls_informatin(outfo[11:])
			elif outfo.find("https")>=0 and outfo.find("www")>=0:
				gather_each_Urls_informatin(outfo[12:])
			elif outfo.find("http")>=0 and not outfo.find("www")>=0:
				gather_each_Urls_informatin(outfo[7:])
			elif outfo.find("https")>=0 and not outfo.find("www")>=0:
				gather_each_Urls_informatin(outfo[8:])
			else:
				print ("https://www.example.com or http://www.example.com")

def gather_url(infos):
	if str(type(info)).find("list")>0:
		processing_Dummy(infos)
	elif str(type(info)).find("str")>0:
		info=infos.strip()
		if info.find("http")==0 and info.find("www")>=0:
			gather_each_Urls_informatin(info[11:])
		elif info.find("https")==0 and info.find("www")>=0:
			gather_each_Urls_informatin(info[12:])
		elif info.find("http")==0 and not info.find("www")>=0:
			gather_each_Urls_informatin(info[7:])
		elif info.find("https")==0 and not info.find("www")>=0:
			gather_each_Urls_informatin(info[8:])
		elif info.find(":\\")<2 and info.find(":\\")>0:
			try:
				filex=open(info,'r+')
				info_page=[lists.strip() for lists in filex.readlines()]
				filex.close()
				processing_Dummy(info_page)
			except Exception,e:
				print (e)
		else:
			print ("Error Url or path")

def gather_toplist(info):
	if str(type(info)=="<type 'str'>"):
		gather_what_kind_of_toplist_you_wander(info)
	else:
		print ("Info must be a Url")

def gather_topkind():
	gather_the_top_type_in_the_kind()




def processing_Dummy(info):
	Pools=Pool(16)
	templist=[]
	if str(type(info))=="<type 'list'>":
		Pools.map(gather_url,info)
		Pools.close()
	elif str(type(info))=="<type 'str'>":
		templist.append(info)
		Pools.map(gather_url,templist)
		Pools.close()
	else:
		print ("error only str or list avaliable")


	
if __name__ == '__main__':
	#gather_what_kind_of_toplist_you_wander('http://top.chinaz.com/hangye/index_yule.html')
	#gather_the_top_type_in_the_kind()
	processing_Dummy("http://www.qq.com")
	info=sys.argv[1:]
	auto_function(info)


"""
we should check out if the list was empty; yes-wait a moment; no-keep on do this
"""

"""
actually we can import an modules from our files
like:
import sys
sys.path.append("your modulse path")
import your modulse name

But you can do so when your modules are only in python library

when the modules was replicative
like(want to import module b):
import sys; 
if not "/home/a/" in sys.path:
    sys.path.append("/home/a/") 
if not 'b' in sys.modules:
    b = __import__('b')
else:
    eval('import b')
    b = eval('reload(b)')
"""