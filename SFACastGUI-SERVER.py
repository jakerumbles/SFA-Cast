import sys
import os
from tkinter import *


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
    os.system('python3 projector.py')

runButton = Button(tk, text='START', width=20, font =('Arial',26), fg='purple4', command=run) #Start button
runButton.pack()
exitButton = Button(tk, text='EXIT', width=20, font =('Arial',26), fg='purple4', command=tk.destroy) #Exit button
exitButton.pack()


tk.mainloop()
mainloop() 