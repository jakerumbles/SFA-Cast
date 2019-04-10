import sys
import os
from tkinter import *

pathname = "~/Desktop" #Defaults path to Desktop if not changed

# GUI Intialization and header
def pathdesk():
    pathname = "~/Desktop"
def pathdoc():
    pathname = "~/Documents"
def pathpic():
    pathname = "~/Pictures"
def run():
    os.system('python p_client.py')
def opendir():
    direct = os.path.expanduser(pathname)
    newpath = direct + "/SFACAST-Screenshots"
    if not os.path.exists(newpath):
        os.makedirs(newpath)


tk = Tk()  
tk.title('SFA-Cast') 
# Taskbar / Menu 
menu = Menu(tk)
tk.config(menu=menu)
file = Menu(menu) #File - Exit
file.add_command(label="Exit", command=tk.destroy)
menu.add_cascade(label="File", menu=file)
edit = Menu(menu) #Change Screenshot path location
edit.add_command(label="Desktop", command = pathdesk)
edit.add_command(label="Documents", command = pathdoc)
edit.add_command(label="Pictures", command = pathpic)
menu.add_cascade(label="Change Screenshot Location", menu=edit)
helper = Menu(menu) # Helper txt file open
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

runButton = Button(tk, text='START', width=20, font =('Arial',26), fg='purple4', command=run) #Start button
runButton.pack()
picButton = Button(tk, text='SCREENSHOT',font =('Arial',26), width=20, fg='purple4',) #See Screenshots button
picButton.pack()
openpicButton = Button(tk, text='SCREENSHOT LIBRARY',font =('Arial',26), width=20, fg='purple4', command=opendir) #See Screenshots button
openpicButton.pack()
exitButton = Button(tk, text='EXIT', width=20, font =('Arial',26), fg='purple4', command=tk.destroy) #Exit button
exitButton.pack()


tk.mainloop()
mainloop() 