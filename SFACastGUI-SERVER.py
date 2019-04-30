import sys
import os
from tkinter import *
import threading

tk = Tk()  

tk.title('SFA-Cast (SERVER)') 
window = Canvas(tk, width=400, height=0) 
window.pack()

menu = Menu(tk)
tk.config(menu=menu)
file = Menu(menu)
file.add_command(label="Exit", command=tk.destroy)
menu.add_cascade(label="File", menu=file)
helper = Menu(menu)
helper.add_command(label="Info")
menu.add_cascade(label="Help", menu=helper)

frame = Frame(tk, width=600, height=400, background='white')
frame.pack_propagate(0)    
frame.pack()
img = PhotoImage(file='sfacast.png')
pic = Label(frame, image=img)
pic.pack()

def run():
    os.system('py p_server.py')

#Start cast thread
def start_cast():
    cast_t = threading.Thread(target=run, args=())
    cast_t.start()

def quit(cast_t):
    os._exit(0)
    tk.destroy()

def start_quit():
    quit_t = threading.Thread(target=quit, args=())
    quit_t.start()

runButton = Button(tk, text='START', width=20, font =('Arial',26), fg='purple4', command=start_cast) #Start button
runButton.pack()
exitButton = Button(tk, text='EXIT', width=20, font =('Arial',26), fg='purple4', command=quit) #Exit button
exitButton.pack()


tk.mainloop()
mainloop() 