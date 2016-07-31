# -*- coding: UTF-8 -*-
import Tkinter
root = Tkinter.Tk()
root.title("KOHAT-Scan") 

'''流程
1.基础部件 退出 最大化 最小化 窗口化
2.基本功能 拉伸放大 子窗口的切换
3.子窗口内布局 迟点详细画 先弄到基础部件和父窗口布局

参考界面 github

'''

width=1000
height=600
w = root.winfo_screenwidth()
h = root.winfo_screenheight()
widths=[1000]

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
		canvas.configure(bg = "#1a1717")
		root.bind('<Button-1>',self.returned)
		canvas.configure(highlightthickness = 0)
		canvas.bind("<B1-Motion>",self.move)
		canvas.bind("<Button-1>",self.button_1)
		canvas.pack()

	def main_button(self):
		#—————————————————————————————— close windows button
		global buttonmaxsize,buttonclose,buttonsmall
		buttonwidth=30
		buttonheight=30

		buttonclose=Tkinter.Button(root, text='X', command=main_windows().close,bg='#1a1717',relief='flat',font=12,activebackground='#d61c1c',fg='white')#relief指定按钮边界类型 bg是背景颜色
		buttonclose.bind('<Enter>',self.change_close)
		buttonclose.bind('<Button-1>',self.click_close)
		buttonclose.bind('<Leave>',self.changebg2)
		buttonclose.pack()
		buttonclose.place(bordermode='inside',height=buttonheight, width=buttonheight,x=(widths[-1]-buttonheight*1))

		buttonsmall=Tkinter.Button(root, text='__', command=main_windows().click_minisize,bg='#1a1717',relief='flat',activebackground='#46A3FF',fg='white')
		buttonsmall.bind('<Enter>',self.change_small)
		buttonsmall.bind('<Leave>',self.changebg2)
		buttonsmall.pack()
		buttonsmall.place(bordermode='inside',height=buttonheight, width=buttonheight,x=(widths[-1]-buttonheight*3))

		buttonmaxsize=Tkinter.Button(root, text='~', command=main_windows().change,bg='#1a1717',relief='flat',activebackground='#46A3FF',fg='white')
		buttonmaxsize.bind('<Enter>',self.changebg_maxsize)
		buttonmaxsize.bind('<Leave>',self.changebg2)
		buttonmaxsize.pack()
		buttonmaxsize.place(bordermode='inside',height=buttonheight, width=buttonheight,x=(widths[-1]-buttonheight*2))


	def change(self):
		global buttonmaxsize
		if buttonmaxsize['text']=='~':
			buttonmaxsize['text']='-'
			main_windows().maxsize()
			widths.append(1280)
			root.update_idletasks()#？？？？？？？？？？？？？？？？？？？？？？
		else:
			main_windows().origin_size()
			buttonmaxsize['text']='~'
			widths.append(1000)
#----------------------------------------------------------------鼠标划过
	def changebg_maxsize(self,event):
		global buttonmaxsize
		buttonmaxsize['bg']='#46A3FF'

	def change_close(self,event):
		global buttonclose
		buttonclose['bg']='#ff0000'

	def change_small(self,event):
		global buttonsmall
		buttonsmall['bg']='#46A3FF'

#鼠标按完后恢复
	def changebg2(self,event):
		global buttonmaxsize,buttonclose,buttonsmall
		buttonmaxsize['bg']='#1a1717'
		buttonclose['bg']='#1a1717'
		buttonsmall['bg']='#1a1717'
#按下效果
	def click_close(self,event):
		global buttonclose
		buttonclose['bg']='#46A3FF'



#移动窗口 这个完全是百度出来的 因为高三八月一就要开学了
	def move(self,event):
		global x,y
		new_x = (event.x-x)+root.winfo_x()
		new_y = (event.y-y)+root.winfo_y()
		s = str(width)+'x'+str(height)+'+'+str(new_x)+"+"+str(new_y)
		root.geometry(s)
	def button_1(self,event):
		global x,y
		x,y = event.x,event.y


	def Menu():
		menubar = Menu(root)
		menubar.add_command(label="Hello!", command=hello)
		menubar.add_command(label="Quit!", command=root.quit)  


#功能模块_

class tester:
	def Frame(self):
		Frames=Tkinter.Frame(height=600,width=100)
		Frames.pack()


#_________________________________________________做个切换窗口 还是做个 选项按钮的
	



main_windows().baseUI()
main_windows().main_button()
tester().Frame()
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
