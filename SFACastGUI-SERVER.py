# GUI for SFA-CAST Server code
# by: Emalee, Ruben, and Jake
# Main Functions: Run code and exit.
# #

import sys
import os
from tkinter import *
import threading
import platform

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


# Gets the Operating System the computer is running 
# Ex: "Windows", "Darin" - for Mac, "Linux" #
def getOS():
        ostype = platform.system()
        return ostype

# Runs/Launches the code by passing a command to the command line
# The getos() is used here because different OS systems use different commands#
def run():
        ostype = getOS()
        if(ostype == 'Windows'):
                os.system('py TCP_server.py')
        else:
                os.system("python3 TCP_server.py")

#Start cast thread
def start_cast():
    cast_t = threading.Thread(target=run, args=())
    cast_t.start() 

# Destorys the open windows and the open GUI
def quit():
    os._exit(0)
    tk.destroy()

# Threads to quit and close all windows
def start_quit():
    quit_t = threading.Thread(target=quit, args=())
    quit_t.start()

# Run Button
runButton = Button(tk, text='START', width=20, font =('Arial',26), fg='purple4', command=start_cast) #Start button
runButton.pack()
# Exit Button
exitButton = Button(tk, text='EXIT', width=20, font =('Arial',26), fg='purple4', command=quit) #Exit button
exitButton.pack()


tk.mainloop()
mainloop() 