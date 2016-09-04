# -*- coding: UTF-8 -*-
import Tkinter,ttk
from PIL import ImageTk,Image
import sys,os

root = Tkinter.Tk()
root.title("KOHAT-Scan") 
ttk.Style().configure("CB.TButton", padding=0, relief="flat",
   background="white")#ttk样式

'''root.attributes("-topmost", 1)'''#置顶


'''流程
1.基础部件 退出 最大化 最小化 窗口化
2.基本功能 拉伸放大 子窗口的切换
3.子窗口内布局 迟点详细画 先弄到基础部件和父窗口布局
参考界面 github

项目更改我打算采用选项的方式来启动渗透功能
左侧栏将只有四大功能布局
kohatspider(在功能按钮下将会列出正在执行或已经完成的任务 完成的任务将会显示灰色 正在执行的任务将会是浅蓝色 完成但未查看的按钮是红色或深蓝色)
comobox+treeview+scrollbar

渗透功能(在功能按钮下将会列出正在执行或已经完成的任务 完成的任务将会显示灰色 正在执行的任务将会是浅蓝色 完成但未查看的按钮是红色或深蓝色)
treeview+notebook(看情况因为有左侧显示可能不用notebook功能)+scrollbar+comobox


信息收集
listbox+comobox+text或Lable


设置
设置功能可能要弄的比较多 这功能要设置爬虫策略(爬行间隔 过滤那些网址等)这就要用选项+textbox
渗透功能的检测项 开启哪些关闭哪些
窗口大小 是否置顶
还可以设置bypass语句文件路径 poc文件路径


界面切换 部件是方法 place_forget() → place() →place_forget() 或者destroy  意思就是隐藏重现隐藏重现真特么神奇 饱读教程并实践才是道理啊

如果能获取当前窗口情况或许能用 place_forget()来控制窗口自定义缩放后按钮的位置
'''

#获取本地路径
path = os.path.abspath(sys.argv[0])[:-16]


#普通状态下的图标
icon_windows = ImageTk.PhotoImage(file = str(path)+r"img\main Button\windows.jpg")
icon_maxsize = ImageTk.PhotoImage(file = str(path)+r"img\main Button\maxsize.jpg")
icon_minsize = ImageTk.PhotoImage(file = str(path)+r"img\main Button\minisize.jpg")
icon_close = ImageTk.PhotoImage(file = str(path)+r"img\main Button\close.jpg")
#划过时候图标
icon_windows_slip = ImageTk.PhotoImage(file = str(path)+r"img\main Button\windows_slip.jpg")
icon_maxsize_slip = ImageTk.PhotoImage(file = str(path)+r"img\main Button\maxsize_slip.jpg")
icon_minsize_slip = ImageTk.PhotoImage(file = str(path)+r"img\main Button\minisize_slip.jpg")
icon_close_slip = ImageTk.PhotoImage(file = str(path)+r"img\main Button\close_slip.jpg")
#按下时候图标
icon_windows_push = ImageTk.PhotoImage(file = str(path)+r"img\main Button\windows_push.jpg")
icon_maxsize_push = ImageTk.PhotoImage(file = str(path)+r"img\main Button\maxsize_push.jpg")
icon_minsize_push = ImageTk.PhotoImage(file = str(path)+r"img\main Button\minisize_push.jpg")
icon_close_push = ImageTk.PhotoImage(file = str(path)+r"img\main Button\close_push.jpg")

width=1200
height=600
w = root.winfo_screenwidth()
h = root.winfo_screenheight()
widths=[1200]

class main_windows: #只是为了做区分建了个类 

	def __init__(self):
		self.top=root
		self.top.bind('<Configure>',self.resize)

	def resize(self,event):
		widths.append(event.width)


	def maxsize(self):
		root.state("zoomed")
		main_windows().tk_forgetA()
		#最大化但是要想到捕抓当前窗口大小的方法


	def origin_size(self):
		root.state("normal")
		main_windows().tk_forgetB()
		#普通窗口模式 还有其他几个模式normal, iconic, withdrawn, or zoomed 打错东西就会回显能有啥模式选吼吼


	def close(self):
		root.quit()
		root.destroy()
		#关闭主体

		
	def click_minisize(self):
		root.overrideredirect(False)
		root.iconify()

	def returned(self,event):
		root.overrideredirect(True)

#移动窗口已经有办法 现在要解决下最小化 方法就是先overrideredirect为假 然后缩小 放大后又恢复为真值 这就要求当我们点击时候要假值变成真值
	def baseUI(self):
		root.resizable(True,True)
		root.overrideredirect(True)
		root.attributes("-alpha",1)# 1是透明度为0% 0是透明度为100%
		root.geometry(str(width)+'x'+str(height)+'+10+10')#窗口大小 长*宽
		canvas = Tkinter.Canvas(root)
		canvas.configure(width = w)
		canvas.configure(height = h)
		canvas.configure(bg = color1)
		root.bind('<Button-1>',self.returned)
		canvas.configure(highlightthickness = 0)
		canvas.bind("<B1-Motion>",self.move)
		canvas.bind("<Button-1>",self.button_1)
		canvas.pack()

	def main_button(self):#tkinter样式 感觉效果比ttk好 把bd弄成0就没阴影了
		global buttonmaxsizeA,buttoncloseA,buttonsmallA
		buttonwidth=30
		buttonheight=30

		buttoncloseA=Tkinter.Button(root, image=icon_close, command=main_windows().close,bg=color1,relief='flat',font=12,activebackground='white',fg=wordcolor,bd=0)#relief指定按钮边界类型 bg是背景颜色
		buttoncloseA.bind('<Enter>',self.change_close)
		buttoncloseA.bind('<Button-1>',self.click_close)
		buttoncloseA.bind('<Leave>',self.changebg2)
		buttoncloseA.place(bordermode='inside',height=buttonheight, width=buttonheight,x=(widths[-1]-buttonheight*1))

		buttonsmallA=Tkinter.Button(root, image=icon_minsize, command=main_windows().click_minisize,bg=color1,relief='flat',activebackground='white',fg=wordcolor,bd=0)
		buttonsmallA.bind('<Enter>',self.change_small)
		buttonsmallA.bind('<Button-1>',self.click_minisizeS)
		buttonsmallA.bind('<Leave>',self.changebg2)
		buttonsmallA.place(bordermode='inside',height=buttonheight, width=buttonheight,x=(widths[-1]-buttonheight*3))
#最大化
		buttonmaxsizeA=Tkinter.Button(root, image=icon_maxsize, command=main_windows().maxsize,bg=color1,relief='flat',activebackground='white',fg=wordcolor,bd=0)
		buttonmaxsizeA.bind('<Enter>',self.changebg_maxsize)
		buttonmaxsizeA.bind('<Button-1>',self.click_maxsize)
		buttonmaxsizeA.bind('<Leave>',self.changebg2)
		buttonmaxsizeA.place(height=buttonheight, width=buttonheight,x=(widths[-1]-buttonheight*2))

	def main_buttonS(self):#最大化时候的情况
		global buttonwindowsB,buttoncloseB,buttonsmallB
		buttonwidth=30
		buttonheight=30

		buttoncloseB=Tkinter.Button(root, image=icon_close, command=main_windows().close,bg=color1,relief='flat',font=12,activebackground='white',fg=wordcolor,bd=0)#relief指定按钮边界类型 bg是背景颜色
		buttoncloseB.bind('<Enter>',self.change_closeB)
		buttoncloseB.bind('<Button-1>',self.click_closeB)
		buttoncloseB.bind('<Leave>',self.changebg3)
		buttoncloseB.place_forget()


		buttonsmallB=Tkinter.Button(root, image=icon_minsize, command=main_windows().click_minisize,bg=color1,relief='flat',activebackground='white',fg=wordcolor,bd=0)
		buttonsmallB.bind('<Enter>',self.change_smallB)
		buttonsmallB.bind('<Button-1>',self.click_minisizeB)
		buttonsmallB.bind('<Leave>',self.changebg3)
		buttonsmallB.place_forget()

#窗口化
		buttonwindowsB=Tkinter.Button(root, image=icon_windows, command=main_windows().origin_size,bg=color1,relief='flat',activebackground='white',fg=wordcolor,bd=0)
		buttonwindowsB.bind('<Enter>',self.changebg_maxsizeB)
		buttonwindowsB.bind('<Button-1>',self.click_windows)
		buttonwindowsB.bind('<Leave>',self.changebg3)
		buttonwindowsB.place_forget()




	def tk_forgetA(self):
		global buttonmaxsizeA,buttoncloseA,buttonsmallA,buttonwindowsB,buttoncloseB,buttonsmallB
		buttonmaxsizeA.place_forget()
		buttoncloseA.place_forget()
		buttonsmallA.place_forget()

		buttonwidth=30
		buttonheight=30
		buttoncloseB.place(bordermode='inside',height=buttonheight, width=buttonheight,x=(w-buttonheight*1))
		buttonsmallB.place(bordermode='inside',height=buttonheight, width=buttonheight,x=(w-buttonheight*3))
		buttonwindowsB.place(bordermode='inside',height=buttonheight, width=buttonheight,x=(w-buttonheight*2))



	def tk_forgetB(self):
		global buttonmaxsizeA,buttoncloseA,buttonsmallA,buttonwindowsB,buttoncloseB,buttonsmallB
		buttonwindowsB.place_forget()
		buttoncloseB.place_forget()
		buttonsmallB.place_forget()
		buttonwidth=30
		buttonheight=30		
		buttoncloseA.place(bordermode='inside',height=buttonheight, width=buttonheight,x=(widths[0]-buttonheight*1))
		buttonsmallA.place(bordermode='inside',height=buttonheight, width=buttonheight,x=(widths[0]-buttonheight*3))
		buttonmaxsizeA.place(bordermode='inside',height=buttonheight, width=buttonheight,x=(widths[0]-buttonheight*2))




#鼠标划过 时效果
	def changebg_maxsize(self,event):
		global buttonmaxsizeA
		buttonmaxsizeA['image']=icon_maxsize_slip
	def changebg_maxsizeB(self,event):
		global buttonwindowsB
		buttonwindowsB['image']=icon_windows_slip

	def change_close(self,event):
		global buttoncloseA
		buttoncloseA['image']=icon_close_slip

	def change_closeB(self,event):
		global buttoncloseB
		buttoncloseB['image']=icon_close_slip

	def change_small(self,event):
		global buttonsmallA
		buttonsmallA['image']=icon_minsize_slip

	def change_smallB(self,event):
		global buttonsmallB
		buttonsmallB['image']=icon_minsize_slip

#鼠标按完后恢复
	def changebg2(self,event):
		global buttonmaxsizeA,buttoncloseA,buttonsmallA
		buttonmaxsizeA['image']=icon_maxsize
		buttoncloseA['image']=icon_close
		buttonsmallA['image']=icon_minsize
	def changebg3(self,event):
		global buttonwindowsB,buttoncloseB,buttonsmallB
		buttonwindowsB['image']=icon_windows
		buttoncloseB['image']=icon_close
		buttonsmallB['image']=icon_minsize
#按下效果
	def click_close(self,event):
		global buttoncloseA
		buttoncloseA['image']=icon_close_push
	def click_closeB(self,event):
		global buttoncloseB
		buttoncloseB['image']=icon_close_push
	def click_minisizeS(self,event):
		global buttonsmallA
		buttonsmallA['image']=icon_minsize_push
	def click_minisizeB(self,event):
		global buttonsmallB
		buttonsmallB['image']=icon_minsize_push

	def click_maxsize(self,event):
		global buttonmaxsizeA
		buttonmaxsizeA['image']=icon_maxsize_push

	def click_windows(self,event):
		global buttonwindowsB
		buttonwindowsB['image']=icon_windows_push




#移动窗口
	def move(self,event):
		global x,y
		new_x = (event.x-x)+root.winfo_x()
		new_y = (event.y-y)+root.winfo_y()
		s = str(width)+'x'+str(height)+'+'+str(new_x)+"+"+str(new_y)
		root.geometry(s)
	def button_1(self,event):
		global x,y
		x,y = event.x,event.y

#菜单 可选
	def Menu():
		menubar = Menu(root)
		menubar.add_command(label="Hello!", command=hello)
		menubar.add_command(label="Quit!", command=root.quit)  


#功能模块_
#测试模块界面 基础边框划分

class tester_frame:
	def Frame(self):
		frame = Tkinter.Frame(root,bg='gray')
		frame.place(x=heightz,y=40,height=height-40*2,width=width-60)


#测试模块功能按钮 每个功能有自己界面 所以我每个独立出一个类来调用
color1='white' #基本要色
color2='#cccccc' #划过时候颜色 仅限于非主题框按钮
color3='#46A3FF' #按下时候颜色 仅限于非主题框按钮
wordcolor='black'
widthz=40
heightz=220
fontsize=None

class KOHAT_spider:
	def kohat_spider(self):
		global buttonk
		buttonk=Tkinter.Button(root, text='KOHAT spider', command=KOHAT_spider().functional_module_spider,bg=color1,relief='flat',bd=0,fg=wordcolor,activebackground=color3,font=fontsize)
		buttonk.bind('<Enter>',self.color)
		buttonk.bind('<Leave>',self.color2)
		buttonk.place(bordermode='inside',height=widthz, width=heightz,y=(widthz*2-40))

	def color(self,event):
		global buttonk
		if not buttonk['bg']==color3:
			buttonk['bg']=color2
		else:
			pass

	def color2(self,event):
		global buttonk
		if not buttonk['bg']==color3:
			buttonk['bg']=color1
		else:
			pass

	def  functional_module_spider(self):
		global buttonk
		click_testerpart()
		buttonk['bg']=color3

	def spider_part(self):
		Spider_entry=Tkinter.Entry(frame,bd=0)
		Spider_entry.place()

class test_part:
	def test_part(self):
		global tester
		tester=Tkinter.Button(root, text='Tester', command=test_part().functional_module_tester,bg=color1,relief='flat',bd=0,fg=wordcolor,activebackground=color3,font=fontsize)
		tester.bind('<Enter>',self.color)
		tester.bind('<Leave>',self.color2)
		tester.place(bordermode='inside',height=widthz, width=heightz,y=(widthz*6-20))


	def color(self,event):
		global tester
		if not tester['bg']==color3:
			tester['bg']=color2
		else:
			pass

	def color2(self,event):
		global tester
		if not tester['bg']==color3:
			tester['bg']=color1
		else:
			pass

	def  functional_module_tester(self):
		global tester
		click_testerpart()
		tester['bg']=color3

	def tester_part(self):
		pass

class information_collect:
	def information_collect(self):
		global information_collecter
		information_collecter=Tkinter.Button(root, text='information', command=information_collect().functional_module_information_collecter,bg=color1,relief='flat',bd=0,fg=wordcolor,activebackground=color3,font=fontsize)
		information_collecter.bind('<Enter>',self.color)
		information_collecter.bind('<Leave>',self.color2)
		information_collecter.place(bordermode='inside',height=widthz, width=heightz,y=(widthz*10-20))


	def color(self,event):
		global information_collecter
		if not information_collecter['bg']==color3:
			information_collecter['bg']=color2
		else:
			pass

	def color2(self,event):
		global information_collecter
		if not information_collecter['bg']==color3:
			information_collecter['bg']=color1
		else:
			pass

	def  functional_module_information_collecter(self):
		global information_collecter
		click_testerpart()
		information_collecter['bg']=color3

	def tester_part(self):
		pass



class opinion:
	def opinion(self):
		global opinion
		opinion=Tkinter.Button(root, text='opinion', command=opinion().functional_module_opinion,bg=color1,relief='flat',bd=0,fg=wordcolor,activebackground=color3,font=fontsize)
		opinion.bind('<Enter>',self.color)
		opinion.bind('<Leave>',self.color2)
		opinion.place(bordermode='inside',height=widthz, width=heightz,y=(widthz*11-20))


	def color(self,event):
		global opinion
		if not opinion['bg']==color3:
			opinion['bg']=color2
		else:
			pass

	def color2(self,event):
		global opinion
		if not opinion['bg']==color3:
			opinion['bg']=color1
		else:
			pass

	def  functional_module_opinion(self):
		global opinion
		click_testerpart()
		opinion['bg']=color3

	def tester_part(self):
		pass



#用于界面优化功能 详情看前面的流程
def click_testerpart():
	'''
	global button_Xpath_injection,button_SSRF,button_sql_injection,button_Json_injection,button_poc_test,button_HTTP_header_pollute
	global button_Logical_vulnerability,button_xss_injection,button_Xml_injection,button_ftp_weak_password,button_Arbitrary_file_downloa_or_upload
	'''
	global buttonk,tester,information_collecter
	opinion['bg']=color1
	tester['bg']=color1
	information_collecter['bg']=color1
	'''
	button_Xpath_injection['bg']=color1
	button_SSRF['bg']=color1
	button_sql_injection['bg']=color1
	button_Json_injection['bg']=color1
	button_poc_test['bg']=color1
	button_HTTP_header_pollute['bg']=color1
	button_Logical_vulnerability['bg']=color1
	button_xss_injection['bg']=color1
	button_Xml_injection['bg']=color1
	button_ftp_weak_password['bg']=color1
	button_Arbitrary_file_downloa_or_upload['bg']=color1
	'''
	buttonk['bg']=color1


def start_test_button():
	KOHAT_spider().kohat_spider()
	test_part().test_part()
	information_collect().information_collect()
	opinion().opinion()

	'''
	sql_injection().sql_injection()
	xss_injection().xss_injection()
	ftp_weak_password().ftp_weak_password()
	SSRF().SSRF()
	Logical_vulnerability().Logical_vulnerability()
	Arbitrary_file_download_or_upload().Arbitrary_file_download_or_upload()
	Xpath_injection().Xpath_injection()
	Xml_injection().Xml_injection()
	Json_injection().Json_injection()
	HTTP_header_pollute().HTTP_header_pollute()
	poc_test().poc_test()
'''


if __name__ == '__main__':
	main_windows().baseUI()
	main_windows().main_button()
	main_windows().main_buttonS()
	tester_frame().Frame()
	start_test_button()
	'''
	tester_frame().canvas()
	'''
	root.mainloop()


'''
23. 如何设置右键菜单?
	
context_menu = Menu(self.tv, tearoff=0)
context_menu.add_command(label="复制", command=copy_handler)
some_widget.bind('<3>', show_context_menu)
 
def show_context_menu(event):
    context_menu.post(event.x_root,event.y_root)
 
def copy_handler():
    pass
'''