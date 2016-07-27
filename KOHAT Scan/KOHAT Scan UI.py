# -*- coding: UTF-8 -*-
import Tkinter
root = Tkinter.Tk()
root.overrideredirect(True)
#root.attributes("-alpha", 0.3)窗口透明度70 %
root.attributes("-alpha",1)#窗口透明度60 %
root.geometry("600x400+10+10")#窗口大小
canvas = Tkinter.Canvas(root)
canvas.configure(width = 800)
canvas.configure(height = 800)
canvas.configure(bg = "white")
canvas.configure(highlightthickness = 2)
canvas.pack()
x, y = 0, 0
root.mainloop()
