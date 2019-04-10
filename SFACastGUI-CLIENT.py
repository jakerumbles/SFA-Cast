import sys
import os
from tkinter import *
import platform

os = platform.system().lower()

tk = Tk()  

tk.title('SFA-Cast') 
window = Canvas(tk, width=400, height=0) 
window.pack()

menu = Menu(tk)
tk.config(menu=menu)
file = Menu(menu)
file.add_command(label="Exit", command=tk.destroy)
menu.add_cascade(label="File", menu=file)
edit = Menu(menu)
edit.add_command(label="Screenshot Location")
menu.add_cascade(label="Edit", menu=edit)
helper = Menu(menu)
helper.add_command(label="Info")
menu.add_cascade(label="Help", menu=helper)

#Label = Label(tk, text = 'SFA-Cast', font =('Arial Black',40), bg = 'purple4', fg = 'white')
#Label.pack(pady=10,padx=10)

frame = Frame(tk, width=600, height=400, background='white')
frame.pack_propagate(0)    
frame.pack()
img = PhotoImage(file='sfacast.png')
pic = Label(frame, image=img)
pic.pack()

def run():
    os.system('python p_client.py')
    
def opendir():
    desktop = os.path.expanduser("~/Desktop")
    os.startfile(desktop) 

runButton = Button(tk, text='START', width=20, font =('Arial',26), fg='purple4', command=run) #Start button
runButton.pack()
picButton = Button(tk, text='SCREENSHOT LIBRARY',font =('Arial',26), width=20, fg='purple4',) #See Screenshots button
picButton.pack()
openpicButton = Button(tk, text='SCREENSHOT LIBRARY',font =('Arial',26), width=20, fg='purple4', command=opendir) #See Screenshots button
openpicButton.pack()
exitButton = Button(tk, text='EXIT', width=20, font =('Arial',26), fg='purple4', command=tk.destroy) #Exit button
exitButton.pack()


tk.mainloop()
mainloop() 