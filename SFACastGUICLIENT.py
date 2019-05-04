# GUI for SFA-CAST Client code
# by: Emalee, Ruben, and Jake
# Main Functions: Run code, edit path, take screenshot, open screenshot folder, and exit.
# #

import sys
import os
from tkinter import *
import threading
import platform

#pathname = "~/SFACAST-Screenshots" #Defaults path to Desktop if not changed

# pathname() sets the pathnane to .../SFA-CAST/SFACAST-Screenshots 
# This sets it to the file in which the program is#
def pathname():
        pathname = "~/SFA-CAST"
        newpath = pathname + "/SFACAST-Screenshots"
        if not os.path.exists(newpath):
                os.makedirs(newpath)
        return newpath

# Gets the Operating System the computer is running 
# Ex: "Windows", "Darin" - for Mac, "Linux" #
def getOS():
        ostype = platform.system()
        return ostype

# Gets the path to the selected pathname and sets as the global pathname
# The pathname will be from the option buttons in the toolbar# 
def makepath(v):
        global pathname
        pathname = v

# Runs/Launches the code by passing a command to the command line
# The getos() is used here because different OS systems use different commands#
def run():
        ostype = getOS()
        if(ostype == 'Windows'):
                os.system('py TCP_client.py')
        else:
                os.system("python3 TCP_client.py")

# Opens README.md for information on SFA-CAST
def readme():
        os.system('open README.md')

# Opens the help file for help with the screenshotting function
def readme2():
        os.system('open Help.txt')

# Opens the directory where the screenshots are stored. 
# This also sends a command to the command line and has to be OS specific.#
def opendir():
        ostype = getOS()
        direct = os.path.expanduser(pathname())
        if(ostype == 'Windows'):
                os.system("start %s" % direct)
        else:
                os.system("open %s" % direct)
        
# Creates threads and then lets each thread call the start function which runs them.
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

def main():
        tk = Tk()  
        tk.title('SFA-Cast') 

        # Taskbar / Menu 
        menu = Menu(tk)
        tk.config(menu=menu)
        # File > Exit
        file = Menu(menu) #File - Exit
        file.add_command(label="Exit", command=tk.destroy)
        menu.add_cascade(label="File", menu=file)
        # Edit > Change Screenshot Location > Desktop / Documents / Pictures
        edit = Menu(menu) #Change Screenshot path location
        edit.add_command(label="Desktop", command=lambda *args: makepath("~/Desktop"))
        edit.add_command(label="Documents", command=lambda *args: makepath("~/Documents"))
        edit.add_command(label="Pictures", command=lambda *args: makepath("~/Pictures"))
        menu.add_cascade(label="Change Screenshot Location", menu=edit)
        # Help > Info / Screenshot Help
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
        # Logo that we created
        img = PhotoImage(file='sfacast.png')
        pic = Label(frame, image=img)
        pic.pack()

        #Buttons
        # Run Button
        runButton = Button(tk, text='START', width=20, font =('Arial',26), fg='purple4', command=start_cast) #Start button
        runButton.pack()
        # Screenshot Library Button
        picButton = Button(tk, text='SCREENSHOT LIBRARY',font =('Arial',26), width=20, fg='purple4', command=opendir) #Take screenshots button
        picButton.pack()
        # Exit Button 
        exitButton = Button(tk, text='EXIT', width=20, font =('Arial',26), fg='purple4', command=quit) #Exit button
        exitButton.pack()

        tk.mainloop()
        mainloop() 

if __name__ == '__main__':
        main()