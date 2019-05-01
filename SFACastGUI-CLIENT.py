import sys
import os
from tkinter import *
import threading
import platform

pathname = "~/SFACAST-Screenshots" #Defaults path to Desktop if not changed

#Gets the Operating System the computer is running
def getOS():
        ostype = platform.system()
        return ostype
#Gets the path to the selected pathname and sets as the pathname
def makepath(v):
        global pathname
        pathname = v

def run():
        ostype = getOS()
        if(ostype == 'Windows'):
                os.system('py TCP_client.py')
        else:
                os.system("python3 TCP_client.py")

def readme():
        os.system('open README.md')

def readme2():
        os.system('open Help.txt')

def opendir():
        ostype = getOS()
        direct = os.path.expanduser(pathname)
        newpath = direct + "/SFACAST-Screenshots"
        if not os.path.exists(newpath):
                os.makedirs(newpath)
        if(ostype == 'Windows'):
                os.system("start %s" % newpath)
        else:
                os.system("open %s" % newpath)
        
        
def start_cast():
    cast_t = threading.Thread(target=run, args=())
    cast_t.start() 

def quit():
    os._exit(0)
    tk.destroy()

def start_quit():
    quit_t = threading.Thread(target=quit, args=())
    quit_t.start()

#Tkinter initalizaion and name bar
tk = Tk()  
tk.title('SFA-Cast') 

# Taskbar / Menu 
menu = Menu(tk)
tk.config(menu=menu)
file = Menu(menu) #File - Exit
file.add_command(label="Exit", command=tk.destroy)
menu.add_cascade(label="File", menu=file)
edit = Menu(menu) #Change Screenshot path location
edit.add_command(label="Desktop", command=lambda *args: makepath("~/Desktop"))
edit.add_command(label="Documents", command=lambda *args: makepath("~/Documents"))
edit.add_command(label="Pictures", command=lambda *args: makepath("~/Pictures"))
menu.add_cascade(label="Change Screenshot Location", menu=edit)
helper = Menu(menu) # Helper txt file open
helper.add_command(label="Info", command = readme)
helper.add_command(label="Screenshot Help", command = readme2)
menu.add_cascade(label="Help", menu=helper)

#Label Logo
#Label = Label(tk, text = 'SFA-Cast', font =('Arial Black',40), bg = 'purple4', fg = 'white')
#Label.pack(pady=10,padx=10)

#Logo added
frame = Frame(tk, width=600, height=400, background='white')
frame.pack_propagate(0)    
frame.pack()
img = PhotoImage(file='sfacast.png')
pic = Label(frame, image=img)
pic.pack()

#Buttons
runButton = Button(tk, text='START', width=20, font =('Arial',26), fg='purple4', command=start_cast) #Start button
runButton.pack()
picButton = Button(tk, text='SCREENSHOT LIBRARY',font =('Arial',26), width=20, fg='purple4', command=opendir) #Take screenshots button
picButton.pack()
exitButton = Button(tk, text='EXIT', width=20, font =('Arial',26), fg='purple4', command=quit) #Exit button
exitButton.pack()

tk.mainloop()
mainloop() 