# -*- coding: UTF-8 -*-
import Tkinter,ttk
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



界面切换 部件是方法 place_forget() → place() →place_forget()  意思就是隐藏重现隐藏重现真特么神奇 饱读教程并实践才是道理啊

如果能获取当前窗口情况或许能用 place_forget()来控制窗口自定义缩放后按钮的位置
'''

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
		#最大化但是要想到捕抓当前窗口大小的方法


	def origin_size(self):
		root.state("normal")
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
		root.bind('<Button-2>',self.returned)
		canvas.configure(highlightthickness = 0)
		canvas.bind("<B1-Motion>",self.move)
		canvas.bind("<Button-1>",self.button_1)
		canvas.pack()

	def main_button(self):#tkinter样式 感觉效果比ttk好 把bd弄成0就没阴影了
		global buttonmaxsizeA,buttoncloseA,buttonsmallA
		buttonwidth=30
		buttonheight=30

		buttoncloseA=Tkinter.Button(root, text='X', command=main_windows().close,bg=color1,relief='flat',font=12,activebackground='#d61c1c',fg=wordcolor,bd=0)#relief指定按钮边界类型 bg是背景颜色
		buttoncloseA.bind('<Enter>',self.change_close)
		buttoncloseA.bind('<Button-1>',self.click_close)
		buttoncloseA.bind('<Leave>',self.changebg2)
		buttoncloseA.place(bordermode='inside',height=buttonheight, width=buttonheight,x=(widths[-1]-buttonheight*1))

		buttonsmallA=Tkinter.Button(root, text='__', command=main_windows().click_minisize,bg=color1,relief='flat',activebackground='#46A3FF',fg=wordcolor,bd=0)
		buttonsmallA.bind('<Enter>',self.change_small)
		buttonsmallA.bind('<Leave>',self.changebg2)
		buttonsmallA.place(bordermode='inside',height=buttonheight, width=buttonheight,x=(widths[-1]-buttonheight*3))
#最大化
		buttonmaxsizeA=Tkinter.Button(root, text='~', command=main_windows().maxsize,bg=color1,relief='flat',activebackground='#46A3FF',fg=wordcolor,bd=0)
		buttonmaxsizeA.bind('<Enter>',self.changebg_maxsize)
		buttonmaxsizeA.bind('<Leave>',self.changebg2)
		buttonmaxsizeA.bind('<ButtonRelease-1>',self.tk_forgetA)
		buttonmaxsizeA.place(bordermode='inside',height=buttonheight, width=buttonheight,x=(widths[-1]-buttonheight*2))

	def main_buttonS(self):#最大化时候的情况
		global buttonmaxsizeB,buttoncloseB,buttonsmallB
		buttonwidth=30
		buttonheight=30

		buttoncloseB=Tkinter.Button(root, text='X', command=main_windows().close,bg=color1,relief='flat',font=12,activebackground='#d61c1c',fg=wordcolor,bd=0)#relief指定按钮边界类型 bg是背景颜色
		buttoncloseB.bind('<Enter>',self.change_closeB)
		buttoncloseB.bind('<Button-1>',self.click_closeB)
		buttoncloseB.bind('<Leave>',self.changebg2)
		buttoncloseB.place_forget()


		buttonsmallB=Tkinter.Button(root, text='__', command=main_windows().click_minisize,bg=color1,relief='flat',activebackground='#46A3FF',fg=wordcolor,bd=0)
		buttonsmallB.bind('<Enter>',self.change_smallB)
		buttonsmallB.bind('<Leave>',self.changebg2)
		buttonsmallB.place_forget()

#窗口化
		buttonmaxsizeB=Tkinter.Button(root, text='---', command=main_windows().origin_size,bg=color1,relief='flat',activebackground='#46A3FF',fg=wordcolor,bd=0)
		buttonmaxsizeB.bind('<Enter>',self.changebg_maxsizeB)
		buttonmaxsizeB.bind('<Leave>',self.changebg2)
		buttonmaxsizeB.bind('<ButtonRelease-1>',self.tk_forgetB)
		buttonmaxsizeB.place_forget()




	def tk_forgetA(self,event):
		global buttonmaxsizeA,buttoncloseA,buttonsmallA,buttonmaxsizeB,buttoncloseB,buttonsmallB
		buttonmaxsizeA.place_forget()
		buttoncloseA.place_forget()
		buttonsmallA.place_forget()

		buttonwidth=30
		buttonheight=30
		buttoncloseB.place(bordermode='inside',height=buttonheight, width=buttonheight,x=(w-buttonheight*1))
		buttonsmallB.place(bordermode='inside',height=buttonheight, width=buttonheight,x=(w-buttonheight*3))
		buttonmaxsizeB.place(bordermode='inside',height=buttonheight, width=buttonheight,x=(w-buttonheight*2))



	def tk_forgetB(self,event):
		global buttonmaxsizeA,buttoncloseA,buttonsmallA,buttonmaxsizeB,buttoncloseB,buttonsmallB
		buttonmaxsizeB.place_forget()
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
		buttonmaxsizeA['bg']='#46A3FF'
	def changebg_maxsizeB(self,event):
		global buttonmaxsizeB
		buttonmaxsizeB['bg']='#46A3FF'

	def change_close(self,event):
		global buttoncloseA
		buttoncloseA['bg']='#ff0000'

	def change_closeB(self,event):
		global buttoncloseB
		buttoncloseB['bg']='#ff0000'

	def change_small(self,event):
		global buttonsmallA
		buttonsmallA['bg']='#46A3FF'

	def change_smallB(self,event):
		global buttonsmallB
		buttonsmallB['bg']='#46A3FF'

#鼠标按完后恢复
	def changebg2(self,event):
		global buttonmaxsizeA,buttoncloseA,buttonsmallA,buttonmaxsizeB,buttoncloseB,buttonsmallB
		buttonmaxsizeA['bg']=color1
		buttoncloseA['bg']=color1
		buttonsmallA['bg']=color1
		buttonmaxsizeB['bg']=color1
		buttoncloseB['bg']=color1
		buttonsmallB['bg']=color1
#按下效果
	def click_close(self,event):
		global buttoncloseA
		buttoncloseA['bg']='#46A3FF'
	def click_closeB(self,event):
		global buttoncloseB
		buttoncloseB['bg']='#46A3FF'



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
		Frames=Tkinter.Frame(root,height=600,width=100,bg='white')
		Frames.pack(side='left')
	def PanedWindow(self):
		PanedWindow=Tkinter.PanedWindow(orient=VERTICAL)
		PanedWindow.pack(fill='both',expand=1)
	def canvas(self):
		root.geometry(str(widthz)+'x'+str(heightz)+'+10+10')#窗口大小 长*宽
		canvas = Tkinter.Canvas(root)
		canvas.configure(width = w)
		canvas.configure(height = heightz)
		canvas.configure(bg = "#4a4242")
		canvas.configure(highlightthickness = 0)
		canvas.pack()


#测试模块功能按钮 每个功能有自己界面 所以我每个独立出一个类来调用
color1='white' #基本要色
color2='#c7c7c7' #划过时候颜色 仅限于非主题框按钮
color3='#656565' #按下时候颜色 仅限于非主题框按钮
wordcolor='black'
widthz=40
heightz=250
class KOHAT_spider:
	def kohat_spider(self):
		global buttonk
		buttonk=Tkinter.Button(root, text='KOHAT spider', command=None,bg=color1,relief='flat',bd=0,fg=wordcolor,activebackground=color3)
		buttonk.bind('<Enter>',self.color)
		buttonk.bind('<Leave>',self.color2)
		buttonk.pack()
		buttonk.place(bordermode='inside',height=widthz, width=heightz,y=(widthz*2-20))

	def color(self,event):
		global buttonk
		buttonk['bg']=color2

	def color2(self,event):
		global buttonk
		buttonk['bg']=color1


class sql_injection:
	def sql_injection(self):
		global button_sql_injection
		button_sql_injection=Tkinter.Button(root, text='sql injection', command=None,bg=color1,relief='flat',bd=0,fg=wordcolor,activebackground=color3)
		button_sql_injection.bind('<Enter>',self.color)
		button_sql_injection.bind('<Leave>',self.color2)
		button_sql_injection.pack()
		button_sql_injection.place(bordermode='inside',height=widthz, width=heightz,y=(widthz*3-20))

	def color(self,event):
		global button_sql_injection
		button_sql_injection['bg']=color2

	def color2(self,event):
		global button_sql_injection
		button_sql_injection['bg']=color1


class xss_injection:	
	def xss_injection(self):
		global button_xss_injection
		button_xss_injection=Tkinter.Button(root, text='xss injection', command=None,bg=color1,relief='flat',bd=0,activebackground=color3,fg=wordcolor)
		button_xss_injection.bind('<Enter>',self.color)
		button_xss_injection.bind('<Leave>',self.color2)
		button_xss_injection.pack()
		button_xss_injection.place(bordermode='inside',height=widthz, width=heightz,y=(widthz*4-20))

	def color(self,event):
		global button_xss_injection
		button_xss_injection['bg']=color2

	def color2(self,event):
		global button_xss_injection
		button_xss_injection['bg']=color1


class ftp_weak_password:
	def ftp_weak_password(self):
		global button_ftp_weak_password
		button_ftp_weak_password=Tkinter.Button(root, text='ftp weak password', command=None,bg=color1,relief='flat',bd=0,activebackground=color3,fg=wordcolor)
		button_ftp_weak_password.bind('<Enter>',self.color)
		button_ftp_weak_password.bind('<Leave>',self.color2)
		button_ftp_weak_password.pack()
		button_ftp_weak_password.place(bordermode='inside',height=widthz, width=heightz,y=(widthz*5-20))

	def color(self,event):
		global button_ftp_weak_password
		button_ftp_weak_password['bg']=color2

	def color2(self,event):
		global button_ftp_weak_password
		button_ftp_weak_password['bg']=color1


class SSRF:	
	def SSRF(self):
		global button_SSRF
		button_SSRF=Tkinter.Button(root, text='SSRF', command=None,bg=color1,relief='flat',bd=0,fg=wordcolor,activebackground=color3)
		button_SSRF.bind('<Enter>',self.color)
		button_SSRF.bind('<Leave>',self.color2)
		button_SSRF.pack()
		button_SSRF.place(bordermode='inside',height=widthz, width=heightz,y=(widthz*6-20))

	def color(self,event):
		global button_SSRF
		button_SSRF['bg']=color2
	def color2(self,event):
		global button_SSRF
		button_SSRF['bg']=color1


class Logical_vulnerability:	
	def Logical_vulnerability(self):
		global button_Logical_vulnerability
		button_Logical_vulnerability=Tkinter.Button(root, text='Logical vulnerability', command=None,bg=color1,relief='flat',bd=0,activebackground=color3,fg=wordcolor)
		button_Logical_vulnerability.bind('<Enter>',self.color)
		button_Logical_vulnerability.bind('<Leave>',self.color2)
		button_Logical_vulnerability.pack()
		button_Logical_vulnerability.place(bordermode='inside',height=widthz, width=heightz,y=(widthz*7-20))

	def color(self,event):
		global button_Logical_vulnerability
		button_Logical_vulnerability['bg']=color2

	def color2(self,event):
		global button_xss_injection
		button_Logical_vulnerability['bg']=color1

class Arbitrary_file_download_or_upload:	
	def Arbitrary_file_download_or_upload(self):
		global button_Arbitrary_file_downloa_or_upload
		button_Arbitrary_file_downloa_or_upload=Tkinter.Button(root, text='Arbitraryd download/upload', command=None,bg=color1,relief='flat',bd=0,activebackground=color3,fg=wordcolor)
		button_Arbitrary_file_downloa_or_upload.bind('<Enter>',self.color)
		button_Arbitrary_file_downloa_or_upload.bind('<Leave>',self.color2)
		button_Arbitrary_file_downloa_or_upload.pack()
		button_Arbitrary_file_downloa_or_upload.place(bordermode='inside',height=widthz, width=heightz,y=(widthz*8-20))

	def color(self,event):
		global button_Arbitrary_file_downloa_or_upload
		button_Arbitrary_file_downloa_or_upload['bg']=color2

	def color2(self,event):
		global button_Arbitrary_file_downloa_or_upload
		button_Arbitrary_file_downloa_or_upload['bg']=color1

class Xpath_injection:	
	def Xpath_injection(self):
		global button_Xpath_injection
		button_Xpath_injection=Tkinter.Button(root, text='Xpath injection', command=None,bg=color1,relief='flat',bd=0,activebackground=color3,fg=wordcolor)
		button_Xpath_injection.bind('<Enter>',self.color)
		button_Xpath_injection.bind('<Leave>',self.color2)
		button_Xpath_injection.pack()
		button_Xpath_injection.place(bordermode='inside',height=widthz, width=heightz,y=(widthz*9-20))

	def color(self,event):
		global button_Xpath_injection
		button_Xpath_injection['bg']=color2

	def color2(self,event):
		global button_Xpath_injection
		button_Xpath_injection['bg']=color1


class Xml_injection:	
	def Xml_injection(self):
		global button_Xml_injection
		button_Xml_injection=Tkinter.Button(root, text='Xml injection', command=None,bg=color1,relief='flat',bd=0,activebackground=color3,fg=wordcolor)
		button_Xml_injection.bind('<Enter>',self.color)
		button_Xml_injection.bind('<Leave>',self.color2)
		button_Xml_injection.pack()
		button_Xml_injection.place(bordermode='inside',height=widthz, width=heightz,y=(widthz*10-20))

	def color(self,event):
		global button_Xml_injection
		button_Xml_injection['bg']=color2

	def color2(self,event):
		global button_Xml_injection
		button_Xml_injection['bg']=color1


class Json_injection:	
	def Json_injection(self):
		global button_Json_injection
		button_Json_injection=Tkinter.Button(root, text='Json injection', command=None,bg=color1,relief='flat',bd=0,activebackground=color3,fg=wordcolor)
		button_Json_injection.bind('<Enter>',self.color)
		button_Json_injection.bind('<Leave>',self.color2)
		button_Json_injection.pack()
		button_Json_injection.place(bordermode='inside',height=widthz, width=heightz,y=(widthz*11-20))

	def color(self,event):
		global button_Json_injection
		button_Json_injection['bg']=color2

	def color2(self,event):
		global button_Json_injection
		button_Json_injection['bg']=color1

class HTTP_header_pollute:	
	def HTTP_header_pollute(self):
		global button_HTTP_header_pollute
		button_HTTP_header_pollute=Tkinter.Button(root, text='HTTP header pollute', command=None,bg=color1,relief='flat',bd=0,activebackground=color3,fg=wordcolor)
		button_HTTP_header_pollute.bind('<Enter>',self.color)
		button_HTTP_header_pollute.bind('<Leave>',self.color2)
		button_HTTP_header_pollute.pack()
		button_HTTP_header_pollute.place(bordermode='inside',height=widthz, width=heightz,y=(widthz*12-20))

	def color(self,event):
		global button_HTTP_header_pollute
		button_HTTP_header_pollute['bg']=color2

	def color2(self,event):
		global button_HTTP_header_pollute
		button_HTTP_header_pollute['bg']=color1


class poc_test:	
	def poc_test(self):
		global button_poc_test
		button_poc_test=Tkinter.Button(root, text='poc_test', command=None,bg=color1,relief='flat',bd=0,activebackground=color3,fg=wordcolor)
		button_poc_test.bind('<Enter>',self.color)
		button_poc_test.bind('<Leave>',self.color2)
		button_poc_test.pack()
		button_poc_test.place(bordermode='inside',height=widthz, width=heightz,y=(widthz*13-20))


	def color(self,event):
		global button_poc_test
		button_poc_test['bg']=color2

	def color2(self,event):
		global button_xss_injection
		button_poc_test['bg']=color1



def start_test_button():
	KOHAT_spider().kohat_spider()
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
父子窗口的参数传递就类似def 与def 或者 class与class的传递只是要def函数的时候要加入传递功能
每次按下一图时,把存放图片的控件烧毁,即存放PHOTOIMAGE的控件烧毁,
然后再打包,然后再放入图片,再设图片定尺寸,图片尺寸的声名要全局性GLOBAL
如果是单改变某控件的组态,这个实例化了控件,其实还是在内存中的,
你把他一拖,啥缩放就没了(也可能是因为不是全局性的变量)
紧记->烧毁->再打包->再自动设定缩放大小(GLOBAL全局变量) 
'''
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