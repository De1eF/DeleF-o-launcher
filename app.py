import minecraft_launcher_lib
import subprocess
from tkinter import ttk
from tkinter import PhotoImage
import tkinter as tk
from ttkthemes import ThemedTk
from threading import *

latest_version = "1.18.2"

minecraft_directory = "D:/miencraftTest"

def startInstall(callbacks):
    def install(callbacks):
        callbacks["onBegin"]()
        
        def set_status(status: str):
            print(status)

        def set_progress(progress: int):
            if current_max != 0:
                print(f"{progress}/{current_max}")
                callbacks["whenInstall"](progress/current_max*100)


        def set_max(new_max: int):
            global current_max
            current_max = new_max
        
        callback = {
            "setStatus": set_status,
            "setProgress": set_progress,
            "setMax": set_max
        }

        # Make sure, the latest version of Minecraft is installed
        minecraft_launcher_lib.install.install_minecraft_version(latest_version, minecraft_directory, callback=callback)
        
        callbacks["onEnd"]()
    thread = Thread(target=lambda: install(callbacks))
    thread.start()

def launch():
    # Get Minecraft command
    options = minecraft_launcher_lib.utils.generate_test_options()
    minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(latest_version, minecraft_directory, options)

    # Start Minecraft
    subprocess.run(minecraft_command)

def GUI():
    #Window
    m = ThemedTk(theme="equilux")
    m.geometry(f"200x300")
    m.config(bg="gray20")
    m.title("Its a launcher")
    m.resizable(False, False)
    
    bg = PhotoImage(file = "background.png")
    lbl_background = ttk.Label(m, image=bg)
    lbl_background.place(relx=0.5, y=150, anchor="center")
    
    #Launch button
    btn_launch = ttk.Button(m, text="Launch", command=launch)
    btn_launch.place(relx=0.5, y=100, anchor="center")
    
    #Progress bar. Starts hidden and is shown upon install check
    prgrs_install = ttk.Progressbar(m, orient="horizontal", length=180, mode="determinate", takefocus=True, maximum=100)
    prgrs_install["value"] = 0
    
    #Install button and callbacks
    def onInstallBegin():
        btn_install.config(state=tk.DISABLED, text="- - -")
        prgrs_install.place(relx=0.5, y=270, anchor="center")
    
    def whenInstall(progress: int):
        prgrs_install["value"] = progress
        
    def onInstallEnd():
        btn_install.config(state=tk.NORMAL, text="Install")
        prgrs_install.place_forget()
    
    installCallback = {
        "onBegin": onInstallBegin,
        "whenInstall": whenInstall,
        "onEnd": onInstallEnd
    }
    
    btn_install = ttk.Button(m, text="Install", command=lambda:startInstall(installCallback))
    btn_install.place(relx=0.5, y=50, anchor="center")
    
    #Main loop
    m.mainloop()
GUI()
