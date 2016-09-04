# -*- coding: cp936 -*-
import urllib2
import re
import time


#write by kcorlidy  it uses to gether top board.
if __name__ == '__main__':
	send_headers = {
 'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20160101 Firefox/16.0',
 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
 'Connection':'keep-alive'
}
	li=['http://top.chinaz.com/hangye/index_yule.html','http://top.chinaz.com/hangye/index_shopping.html',
	'http://top.chinaz.com/hangye/index_gov.html','http://top.chinaz.com/hangye/index_jiaoyu.html',
	'http://top.chinaz.com/hangye/index_qiye.html','http://top.chinaz.com/hangye/index_shenghuo.html',
	'http://top.chinaz.com/hangye/index_wangluo.html','http://top.chinaz.com/hangye/index_tiyu.html',
	'http://top.chinaz.com/hangye/index_yiliao.html','http://top.chinaz.com/hangye/index_jiaotonglvyou.html',
	'http://top.chinaz.com/hangye/index_news.html']
	dictQ=[]
	dictP=[]
	for i in li:
		Req = urllib2.Request(i,headers=send_headers)
		Page = urllib2.urlopen(Req,timeout=15)
		DOM=Page.read()
		rex=re.findall(r'"'+i[29:-5]+r'[^]*[^<]*',DOM)
		for x in rex:
			try:
				if not x.find('zonghe')>0 and not len(re.findall(r'_\d[^.]*',x))>0 and not x.find('pr.html')>0 and not x.find('br.html')>0 and not x.find('class="tagCurt"')>0 and not x.find('alexa.html')>0 and not x.find('>1')>0:
					dictQ.append(x.split('">'))
					print dictQ
			except:
				pass
		time.sleep(3)
print dictQ
