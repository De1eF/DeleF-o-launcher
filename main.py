import minecraft_launcher_lib
import subprocess
from tkinter import ttk
from tkinter import PhotoImage
import tkinter as tk
from ttkthemes import *
import gdown
import os
import zipfile
import json
import sys
from threading import Thread
from tkinter import StringVar

def boot():
    latest_version = "1.21.1"
    fabric_version = "fabric-loader-0.16.9-1.21.1"
    configDir = dict()
    
    def updateConfig(key: str, value):
        configDir[key] = value
        with open("config.json", "w") as f:
            json.dump(configDir, f)
    
    if not os.path.isfile("config.json"):
        updateConfig("path","C:/DeleF-o-launcher")
        updateConfig("username", "Steve")
        updateConfig("maxRam","2")
        updateConfig("minRam","2")
    with open("config.json", "r") as f:
        configDir = json.loads(f.read())
    minecraft_directory = configDir["path"]
    
    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

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
            callbacks["onStageChange"]("Minecraft")
            minecraft_launcher_lib.install.install_minecraft_version(latest_version, minecraft_directory, callback=callback)
            callbacks["onStageChange"]("Fabric")
            minecraft_launcher_lib.fabric.install_fabric(latest_version, minecraft_directory, callback=callback)
            callback["setProgress"](30)
            callbacks["onStageChange"]("Mods")
            downloadZip("1d82sNK8T_P9lC-XFvhrumYgyI6rBQvj5", minecraft_directory + "/mods.zip")
            callback["setProgress"](60)
            callbacks["onStageChange"]("Resourcepacks")
            downloadZip("1leIHo3DxbhwNEsKGs9HXLSqyKmXOgmkJ", minecraft_directory + "/resourcepacks.zip")
            callback["setProgress"](90)
            callbacks["onStageChange"]("Shaderpacks")
            downloadZip("1OGSX64CGgIgDeoVNMD6ta1C1ohz8v-zA", minecraft_directory + "/shaderpacks.zip")
            
            callbacks["onEnd"]()
        thread = Thread(target=lambda: install(callbacks))
        thread.start()

    def launch():     
        # Get Minecraft command
        options = minecraft_launcher_lib.utils.generate_test_options()
        options["username"] = configDir["username"]
        options["jvmArguments"] = ["-Xmx" + configDir["maxRam"] + "G", "-Xms" + configDir["minRam"] + "G"]
        minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(fabric_version, minecraft_directory, options)

        # Start Minecraft
        subprocess.run(minecraft_command)

    def downloadZip(file_id, destination):
        url = 'https://drive.google.com/uc?id=' + file_id
        gdown.download(url, destination, quiet=False, fuzzy=True)
        
        print("finished downloading")
        
        dir_name = minecraft_directory + '/mods'
        zip_ref = zipfile.ZipFile(destination) # create zipfile object
        zip_ref.extractall(dir_name) # extract file to dir
        zip_ref.close() # close file
        os.remove(destination) # delete zipped file
                

    def GUI():
        #Window
        m = ThemedTk(theme="equilux")
        m.geometry(f"200x300")
        m.config(bg="gray20")
        m.title("Delef-o-launcher")
        m.resizable(False, False)
        m.iconbitmap(resource_path("icon.ico"))
        
        bg = PhotoImage(file = resource_path("background.png"))
        lbl_background = ttk.Label(m, image=bg)
        lbl_background.place(relx=0.5, y=150, anchor="center")
        
        #Username label
        lbl_username = ttk.Label(m, text="Name:")
        lbl_username.place(relx=0.5, x=-25, y=176, anchor="center", width=50, height=20)
        
        #Username entry
        usernameStringVar = StringVar()
        usernameStringVar.trace_add("write", lambda a,b,c: {updateConfig("username", usernameStringVar.get())})
        ntry_username = ttk.Entry(m, textvariable = usernameStringVar)
        ntry_username.place(relx=0.5, x=25, y=176, anchor="center", width=50, height=20)
        ntry_username.insert("0", configDir["username"])
        
        #Path entry
        pathStringVar = StringVar()
        pathStringVar.trace_add("write", lambda a,b,c: {updateConfig("path", pathStringVar.get())})
        ntry_install = ttk.Entry(m, textvariable = pathStringVar)
        ntry_install.place(relx=0.5, y=100, anchor="center", width=100, height=30)
        ntry_install.insert("0",minecraft_directory)
        
        #Launch button
        btn_launch = ttk.Button(m, text="Launch", command=launch)
        btn_launch.place(relx=0.5, y=200, anchor="center", width=100)
        
        lbl_install = ttk.Label(m)
        
        #Progress bar. Starts hidden and is shown upon install check
        prgrs_install = ttk.Progressbar(m, orient="horizontal", length=180, mode="determinate", takefocus=True, maximum=100)
        prgrs_install["value"] = 0
        
        #Install button and callbacks
        def onInstallBegin():
            btn_install.config(state=tk.DISABLED, text="- - -")
            btn_launch.config(state=tk.DISABLED)
            prgrs_install.place(relx=0.5, y=270, anchor="center")
            lbl_install.place(relx=0.5, y=250, anchor="center")
        
        def whenInstall(progress: int):
            prgrs_install["value"] = progress
        
        def onStageChange(stage: str):
            lbl_install.config(text="Now installing: " + stage)
            
        def onInstallEnd():
            btn_install.config(state=tk.NORMAL, text="Install")
            btn_launch.config(state=tk.NORMAL)
            prgrs_install.place_forget()
            lbl_install.place_forget()
        
        installCallback = {
            "onBegin": onInstallBegin,
            "whenInstall": whenInstall,
            "onStageChange": onStageChange,
            "onEnd": onInstallEnd
        }
        
        btn_install = ttk.Button(m, text="Install", command=lambda:startInstall(installCallback))
        btn_install.place(relx=0.5, y=129, anchor="center", width=100)
        
        #Main loop
        m.mainloop()
    GUI()

def main():
    boot()

if __name__ == "__main__":
    main()
