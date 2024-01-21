#10.212.94.65
import socket # == sockets allows to establish network connections over various network protocol
import sys
import threading
import time
from tkinter import *
from tkinter import messagebox
import subprocess
import openai
from apikey import APIKEY


class showPortDetails:
    def __init__(self, target_portnumber):
        # Scan Vars
        self.portnumber_s = 1  # Default
        self.portnumber_f = 1024
        self.log = []
        self.ports = []  # array to store ports
        self.target = target_portnumber # default for portnumber
        self.start_time = None
        self.end_time = None
        self.listbox = None
        # Start GUI
        self.init_gui()
        
     
    def PortDetails(self, target, port):
        print(f"Received target_portnumber in PortDetails: {self.target}")
        self.ports = []
        self.start_time = time.time()
        self.L29.configure(text=time.strftime("%Y-%m-%d %H:%M:%S"))
        try:
            service_name = socket.getservbyport(port, "tcp")
            self.listbox.insert("Port No: {} Service Name: {}".format(port, service_name))
        except (socket.error, OSError):
            self.listbox.insert("Port No: {} Service Name: {}".format(port, "Unknown"))
        if not self.ports:
            self.listbox.insert("end", "No description found on port {}".format(self.target))


            
    def get_wifi_name(self):
        result = subprocess.run(["netsh", "wlan", "show", "interfaces"], capture_output=True, text=True)
        output_lines = result.stdout.split('\n')
        for line in output_lines:
            if "SSID" in line:
                return line.split(":")[1].strip()        
            
    def init_gui(self):
        # ===== START OF GRAPHICAL USER INTERFACE =====
        self.gui = Tk()
        self.gui.title('Port Details')
        self.gui.geometry("400x630+20+20")

        # Colour Palette
        m1c = '#0a0a0a'
        bgc = '#F0FFF0'
        fgc = '#111111'

        self.gui.tk_setPalette(background=bgc, foreground=m1c, activeBackground=fgc, activeForeground=bgc,
                               highlightColor=m1c, highlightBackground=m1c)

        # Page Title
        self.L11 = Label(self.gui, text="Port Selected", font=("Helvetica", 16))
        self.L11.place(x=115, y=10)

        # Get portnumber
        self.L21 = Label(self.gui, text="Port Number: ")
        self.L21.place(x=16, y=60)

        self.L22 = Entry(self.gui)
        self.L22.place(x=180, y=60)
        self.L22.insert(0, self.target)

        # Get the Port Range (By default 1-1024)
        self.L23 = Label(self.gui, text="Ports Range: ")
        self.L23.place(x=16, y=90)

        self.L24 = Entry(self.gui, text="1")
        self.L24.place(x=180, y=90, width=95)
        self.L24.insert(0, "1")

        self.L25 = Entry(self.gui, text="1024")
        self.L25.place(x=290, y=90, width=95)
        self.L25.insert(0, "1024")

        # Display number of open ports
        self.L26 = Label(self.gui, text="Number of Open Ports: ")
        self.L26.place(x=16, y=180)
        self.L27 = Label(self.gui)
        self.L27.place(x=200, y=180)

        # Display start time of the scan
        self.L28 = Label(self.gui, text="Search Start Time:")
        self.L28.place(x=16, y=210)
        self.L29 = Label(self.gui, text="")
        self.L29.place(x=180, y=210)

        # Display end time of the scan
        self.L30 = Label(self.gui, text="Search End Time:")
        self.L30.place(x=16, y=240)
        self.L31 = Label(self.gui, text="")
        self.L31.place(x=180, y=240)

        # Display the run time of the scan
        self.L32 = Label(self.gui, text="Search Duration:")
        self.L32.place(x=16, y=270)
        self.L33 = Label(self.gui, text="")
        self.L33.place(x=180, y=270)

        # Display the list of open ports
        self.L34 = Label(self.gui, text="Port Description :")
        self.L34.place(x=16, y=300)
        frame = Frame(self.gui)
        frame.place(x=16, y=330, width=370, height=200)
        self.listbox = Listbox(frame, width=59, height=12)
        self.listbox.pack(expand=YES, fill=BOTH)
        self.listbox.place(x=0, y=0)
        self.listbox.bind('<<ListboxSelect>>')
        scrollbar = Scrollbar(frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        wifi_name = self.get_wifi_name()
        self.L35 = Label(self.gui, text="Network Connected: " + wifi_name)
        self.L35.place(x=20, y=600)
        
        self.L36 = Label(self.gui, text="**You may specify the port number to investigate.")
        self.L36.place(x=16, y=115)
        
        self.L36 = Label(self.gui, text="Port Details", font=("Helvetica", 14))
        self.L36.place(x=125, y=150)

        # Button for start scan
        self.B11 = Button(self.gui, text="Search Port Details", command=lambda: self.PortDetails())

        self.B11.place(x=16, y=540, width=70)

        # # Button to return to the previous page
        # self.B21 = Button(self.gui, text="Back")
        # self.B21.place(x=90, y=500, width=70)

        # Button for download result
        self.B21 = Button(self.gui, text="Download Result")
        self.B21.place(x=90, y=540, width=100)

        # ==== Start GUI ====
        self.gui.resizable(False, False)
        self.gui.mainloop()
        
        # Create the Back button
        B21 = Button(self.gui, text="Back", command=self.gui.destroy.pack())
        B21.place(x = 90, y = 500, width = 70)
        
scanner = None

def receive_target(target_portnumber):
    global scanner
    print(f"Target Port Number: {target_portnumber}")
    scanner = showPortDetails(target_portnumber)
    messagebox.showinfo("Hello, World!")    