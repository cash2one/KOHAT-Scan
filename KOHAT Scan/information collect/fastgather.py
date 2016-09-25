import urllib2
import re
import time
import sys
import os
import threading
import Queue
import getopt
#write by kcorlidy  it uses to gether top board;information of website(domains,the weight) 

send_headers = {
 'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20160901 Firefox/49.0',
 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
 'Connection':'keep-alive'
}

li=['http://top.chinaz.com/hangye/index_yule.html','http://top.chinaz.com/hangye/index_shopping.html',
	'http://top.chinaz.com/hangye/index_gov.html','http://top.chinaz.com/hangye/index_jiaoyu.html',
	'http://top.chinaz.com/hangye/index_qiye.html','http://top.chinaz.com/hangye/index_shenghuo.html',
	'http://top.chinaz.com/hangye/index_wangluo.html','http://top.chinaz.com/hangye/index_tiyu.html',
	'http://top.chinaz.com/hangye/index_yiliao.html','http://top.chinaz.com/hangye/index_jiaotonglvyou.html',
	'http://top.chinaz.com/hangye/index_news.html']

Q=Queue.Queue()

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
			for Qx in re_urls_fliter:
				Reqx = urllib2.Request("http://rank.chinaz.com/?host="+str(Qx),headers=send_headers)
				Pagex = urllib2.urlopen(Reqx,timeout=15)
				DOMx=Pagex.read()

				#website weight and Subdomain
				re_information_Subdomain=[ismd[29:] for ismd in re.findall(r"http://rank.chinaz.com/.host.[^]*[^>]*",DOMx) if ismd.find(Qx)>0 and ismd.find('Type')<0] # it is domains !
				re_information_weight=[weight[0:weight.find("<")-1]+" "+weight[weight.find('>')+1:] for weight in re.findall(r"\w*.<i id[^]*[<]*",DOMx)] #it is weight !
				
				#website IP adress,physical_address
				ReqY = urllib2.Request("http://ip.chinaz.com/?ip="+str(Qx),headers=send_headers)
				PageY = urllib2.urlopen(ReqY,timeout=15)
				DOMY=PageY.read()

				re_website_IP_address=[ip[24:] for ip in re.findall(r"class=.Whwtdhalf w15-0.[^]*[<]*",DOMY)[2:] if ip.find(".")>0 and not ip.find(Qx)>0] #get ip adress 
				re_website_physical_address=[phy[7:] for phy in re.findall(r'w50-0.{2}[^]*[<]*',DOMY)] #physical_address
				
				#which website under the same IP adress
				ReqZ = urllib2.Request("http://ip.chinaz.com/Same/?s="+str(Qx),headers=send_headers)
				PageZ = urllib2.urlopen(ReqZ,timeout=15)
				DOMZ=PageZ.read()

				re_under_same_IP_adress=[Z[18:] for Z in re.findall(r"overhid.{3}a href.{2}[^]*[^']*",DOMZ)]
				
			
				weight_name=['baidu weight','keywords','IP flow']
				result_files=open(str(Qx)+str(time.ctime().replace(":","_"))+'.md','w+')
				for weights in range(len(re_information_weight)-1):
					result_files.write(weight_name[weights]+":"+re_information_weight[weights]+"\n")
				for ip_adress in range(len(re_website_physical_address)-1):
					result_files.write(re_website_IP_address[ip_adress]+"  "+re_website_physical_address[ip_adress+1]+"\n")
				for Subdomains in range(len(re_information_Subdomain)):
					result_files.write(re_information_Subdomain[Subdomains]+"\n")
				for same_IP in re_under_same_IP_adress:
					result_files.write(same_IP+"\n")
				result_files.close()



#it coulid help you gather witch website information that you wander,list or string only, if you input list this will gather all you input
#i would judge if your input_type
#i dont know how to judge  path or url
def gather_each_Urls_informatin(info_website):
	#for each Urls info and gather information
	if 1:
			for Qx in info_website:
				Reqx = urllib2.Request("http://rank.chinaz.com/?host="+str(Qx),headers=send_headers)
				Pagex = urllib2.urlopen(Reqx,timeout=15)
				DOMx=Pagex.read()

				#website weight and Subdomain
				re_information_Subdomain=[ismd[29:-1] for ismd in re.findall(r"http://rank.chinaz.com/.host.[^]*[^>]*",DOMx) if ismd.find(Qx)>0 and ismd.find('Type')<0] # it is domains !
				re_information_weight=[weight[0:weight.find("<")-1]+" "+weight[weight.find('>')+1:] for weight in re.findall(r"\w*.<i id[^]*[<]*",DOMx)] #it is weight !
				
				#website IP adress,physical_address
				ReqY = urllib2.Request("http://ip.chinaz.com/?ip="+str(Qx),headers=send_headers)
				PageY = urllib2.urlopen(ReqY,timeout=15)
				DOMY=PageY.read()

				re_website_IP_address=[ip[24:] for ip in re.findall(r"class=.Whwtdhalf w15-0.[^]*[<]*",DOMY)[2:] if ip.find(".")>0 and not ip.find(Qx)>0] #get ip adress 
				re_website_physical_address=[phy[7:] for phy in re.findall(r'w50-0.{2}[^]*[<]*',DOMY)] #physical_address
				
				#which website under the same IP adress
				ReqZ = urllib2.Request("http://ip.chinaz.com/Same/?s="+str(Qx),headers=send_headers)
				PageZ = urllib2.urlopen(ReqZ,timeout=15)
				DOMZ=PageZ.read()

				re_under_same_IP_adress=[Z[18:] for Z in re.findall(r"overhid.{3}a href.{2}[^]*[^']*",DOMZ)]

				
				print re_information_weight
				print re_website_IP_address
				print re_website_physical_address
				print re_information_Subdomain
				print re_under_same_IP_adress
				#print len(DOMZ),len(DOMY)
				#print len(re.findall(r"overhid.{3}a href.{2}[^]*[^']*",DOMZ))

				weight_name=['baidu weight','keywords','IP flow']
				result_files=open(str(Qx)+str(time.ctime().replace(":","_"))+'.md','w+')
				for weights in range(len(re_information_weight)-1):
					result_files.write(weight_name[weights]+":"+re_information_weight[weights]+"\n")
				for ip_adress in range(len(re_website_physical_address)-1):
					result_files.write(re_website_IP_address[ip_adress]+"  "+re_website_physical_address[ip_adress+1]+"\n")
				for Subdomains in range(len(re_information_Subdomain)):
					result_files.write(re_information_Subdomain[Subdomains]+"\n")
				for same_IP in re_under_same_IP_adress:
					result_files.write(same_IP+"\n")
				result_files.close()




def auto_function(info):
	templist=[]
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
			filex=open(outfo,'r+')
			info_page=[lists.strip() for lists in filex.readlines()]
			filex.close()
			gather_each_Urls_informatin(info_page)
		elif opt in ("-u", "--url"):
			outfo = arg
			templist.append(outfo)
			if len(templist)>0:
				gather_each_Urls_informatin(templist)

def gather_url(info):
	listx=[]
	if type(info)=="<type 'list'>":
		gather_each_Urls_informatin(info)
	elif type(info)=="<type 'str'>":
		if info.find("www")>0:
			listx.append(info)
			if len(listx)>0:
				gather_each_Urls_informatin(listx)
		elif not info.find("www")>0:
			filex=open(info,'r+')
			info_page=[lists.strip() for lists in filex.readlines()]
			filex.close()
			gather_each_Urls_informatin(info_page)
		else:
			print ("error:Make sure info is str or list")

def gather_toplist(info):
	if type(info)=="<type 'str'>":
		gather_what_kind_of_toplist_you_wander(info)
	else:
		print ("Info must be a Url")

def gather_topkind():
	gather_the_top_type_in_the_kind()

if __name__ == '__main__':
	#gather_what_kind_of_toplist_you_wander('http://top.chinaz.com/hangye/index_yule.html')
	#gather_the_top_type_in_the_kind()
	info=sys.argv[1:]
	auto_function(info)

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
