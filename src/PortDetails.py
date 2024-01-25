import socket # == sockets allows to establish network connections over various network protocol
import sys
import threading
import time
from tkinter import *
from tkinter import messagebox,simpledialog
import subprocess
import openai
import json

class showPortDetails:
    def __init__(self, target_port):
        # Scan Vars
        self.portnumber_s = 1  # Default
        self.portnumber_f = 1024
        self.log = []
        self.ports = []  # array to store ports
        self.target = target_port # default for portnumber

        # Start GUI
        self.init_gui()
            
    def PortDetails(self):
        print(f"Received target_port in PortDetails: {self.target}")
        #To get service name by using getservbyport function
        try:
            service_name = socket.getservbyport(self.target, "tcp")
            # Corrected insert statement
            detail_text = "Port No: {} Service Name: {}".format(self.target, service_name)
            self.text_widget.config(state=NORMAL)  # Set the state to normal to allow editing
            self.text_widget.insert(END, detail_text + "\n\n")
            self.text_widget.config(state=DISABLED)  # Set the state back to disabled (read-only)
            
        except (socket.error, OSError):
            detail_text = "Port No: {} Service Name: {}".format(self.target, "Unknown")
            self.text_widget.config(state=NORMAL)
            self.text_widget.insert(END, detail_text + "\n\n")
            self.text_widget.config(state=DISABLED)
            
        if not self.target:
            description_text = "No description found on port {}".format(self.target)
            self.text_widget.config(state=NORMAL)
            self.text_widget.insert(END, description_text + "\n\n")
            self.text_widget.config(state=DISABLED)
        
            
        #To get port vulnerabilities based on port number by using OpenAI API     
        # Set your OpenAI API key
        #***********************************
        API_KEY = 'REPLACE_WITH_YOUR_OWN_KEY'
        #***********************************
        openai.api_key = API_KEY   
         
        # Define the prompt to the OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  
            messages=[{"role": "user", 
                        "content": "What is the vulnerabilities if port {} is opened".format(self.target) }]
        )

        # Extract the generated text from the API response
        generated_content = response['choices'][0]['message']['content']
        self.text_widget.config(state=NORMAL)
        self.text_widget.insert(END, generated_content+ "\n")
        self.text_widget.config(state=DISABLED)

            
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

        # Display the generated content as normal text with automatic line breaks
        self.L34 = Label(self.gui, text="Port Description :")
        self.L34.place(x=16, y=180)
        frame = Frame(self.gui)
        frame.place(x=16, y=200, width=370, height=300)
        self.text_widget = Text(frame, wrap=WORD, width=56, height=50)
        self.text_widget.pack(expand=YES, fill=BOTH)
        self.text_widget.config(state=DISABLED)  # To make it read-only

        wifi_name = self.get_wifi_name()
        self.L35 = Label(self.gui, text="Network Connected: " + wifi_name)
        self.L35.place(x=20, y=600)
               
        self.L36 = Label(self.gui, text="Port Details", font=("Helvetica", 14))
        self.L36.place(x=125, y=150)

        # Button for start scan
        self.B11 = Button(self.gui, text="Search Port Details", command=lambda: self.PortDetails())
        self.B11.place(x=16, y=540, width=130)

        # ==== Start GUI ====
        self.gui.resizable(False, False)
        self.gui.mainloop()
        
        # Create the Back button
        B21 = Button(self.gui, text="Back", command=self.gui.destroy.pack())
        B21.place(x = 90, y = 500, width = 70)
        
scanner = None

def receive_target(target_port):
    global scanner
    print(f"Target Port Number: {target_port}")
    scanner = showPortDetails(target_port)
    
       
