# -*- coding: UTF-8 -*-
import urllib,urllib2
import re
import threading
import thread
import time
from multiprocessing import Pool
import datetime
path=r"C:\Users\chen1\Desktop\url coleection "+str(datetime.datetime.now())[:19].replace(':','-')+'.txt'
#set urllib2 op
send_headers = {
 'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
 'Connection':'keep-alive'
}
#设置header 备用
'''req = urllib2.Request(url,headers=send_headers)
r = urllib2.urlopen(req)
html = r.read()        #返回网页内容'''


def geteachhtml(words,ints):
    url = "http://www.baidu.com/s"
    search = [('w',words)]
    pnz = [('pn',ints)]
    getString = url + "?" + urllib.urlencode(search)+"&"+urllib.urlencode(pnz)
    req = urllib2.Request(getString)
    fd = urllib2.urlopen(req)
    baiduResponse=""
    while 1:
        data= fd.read(1024)
        if not len(data):
            break
        baiduResponse+=data
    return baiduResponse
def geteachpageurl(words,ints):
    lists=[]
    listB=[]
    surlget=[]
    global re
    Dom=geteachhtml(words,ints)
    p = re.compile(r'\bhttp://www.baidu.com/link\b[^\s]*')
    urlget = re.findall(p,Dom)
    for each in urlget:
         eachurl=each.split('"')[0]
         lists.append(eachurl)
    for n in lists:
        try:
            listB.append(urllib2.urlopen(n).geturl())           
        except Exception, e:
                         pass
    '''print list(set(listB))'''
    files=open(path,'a')
    files.writelines([line+'\n' for line in list(set(listB))])
    files.close()


def urlfilter(strx):
    listf=strs
    lists=[]
    Relist=[]
    filters= []
    for eachblack in Blacklist:
        Relist=re.findall(r"\b"++r"\b[^s]*",str(listf))
        for x in Relist:
            filters.append(x)
    return filters


def threadingpool(words,ints):
    word=words
    pagenumber=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430, 440, 450, 460, 470, 480, 490, 500, 510, 520, 530, 540, 550, 560, 570, 580, 590, 600, 610, 620, 630, 640, 650, 660, 670, 680, 690, 700, 710, 720, 730, 740, 750]
    for i in pagenumber[:int(ints)]:
        '''result.append(thread.start_new_thread(geteachpageurl,(word,i)))'''
        t=threading.Thread(target = geteachpageurl, args = (word,i), name = 'spider' + str(i))
        t.start()
    print 'all start'

def processpool(words,ints):
    result=[]
    word=words
    pagenumber=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430, 440, 450, 460, 470, 480, 490, 500, 510, 520, 530, 540, 550, 560, 570, 580, 590, 600, 610, 620, 630, 640, 650, 660, 670, 680, 690, 700, 710, 720, 730, 740, 750]
    pool = Pool(10)#warning 别开太多进程不然百度认为你攻击呢 然后就断你连接
    for i in pagenumber[:int(ints)]:
        result.append(pool.apply(geteachpageurl,(word,i)))
        time.sleep(1)
    pool.close()
    pool.join()
    print result


if __name__ == '__main__':
    '''whitelist=['http://v.baidu.com/link']'''
    word = raw_input('keyword is:')
    ints = raw_input("how many page(75 was max):")
    '''processpool(word,ints)'''
    threadingpool(word,ints)

"""multiprocess.dummy.pool.map"""
