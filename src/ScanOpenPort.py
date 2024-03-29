import socket
import sys
import threading
import time
from tkinter import *
import subprocess

class NetshieldPortScanner:
    def __init__(self, target_ip):
        # Scan Vars
        self.ip_s = 1  # Default
        self.ip_f = 1024
        self.log = []
        self.ports = []  # array to store ports
        self.target = target_ip # default for port
        self.start_time = None
        self.end_time = None
        self.listbox = None

        # Start GUI
        self.init_gui()
        

    def scan_port(self, target, port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4)
            c = s.connect_ex((target, port))
            if c == 0:
                m = ' Port %d ' % (port,)
                self.ports.append(port)
                self.listbox.insert("end", str(m))  # append to the end of list
                self.update_no_of_open_port()


                # Assuming the `receive_target` function is in the `PortDetails` module
                from PortDetails import receive_target  


                '''# Function to handle button click and send the value to target_portnumber
                def handle_button_click(port):
                    target_port = port
                    receive_target(target_port)

                # Create a button dynamically for each open port
                button = Button(text=">", command=lambda p=port: handle_button_click(p), padx=5, pady=1)
                button.pack(side=TOP)'''

            s.close()
        except OSError:
            print('!!!Too many open sockets. Port ' + str(port) + '!!!')
        except:
            s.close()
            sys.exit()
            
              
    def update_no_of_open_port(self):
        rtext = " [ " + str(len(self.ports)) + " / " + str(self.ip_f) + "]"
        self.L27.configure(text=rtext)
        

    def start_scan(self):
        self.ports = []
        self.start_time = time.time()
        self.L29.configure(text=time.strftime("%Y-%m-%d %H:%M:%S"))
       
        # Get ports ranges from GUI (get the starting point and ending point of ports)
        self.ip_s = int(self.L24.get())
        self.ip_f = int(self.L25.get())

        # Initiates a loop to scan the ports in the specific IP
        while self.ip_s <= self.ip_f:
            try:
                scan = threading.Thread(target=self.scan_port, args=(self.target, self.ip_s))
                scan.setDaemon(True)
                # start the thread
                scan.start()
            except:
                time.sleep(0.01)
            # Increment of the port number
            self.ip_s += 1

        self.end_time = time.time()
        runtime = self.end_time - self.start_time
        self.L31.configure(text=time.strftime("%Y-%m-%d %H:%M:%S"))
        self.L33.configure(text=f"{runtime:.2f} seconds")
        self.log.append(" End Time:\t" + time.strftime("%Y-%m-%d %H:%M:%S"))
        self.log.append(" Runtime:\t{:.2f} seconds".format(runtime))

        if not self.ports:
            self.listbox.insert("end", "No open ports found on IP Address {}".format(self.target))
            

    def get_wifi_name(self):
        result = subprocess.run(["netsh", "wlan", "show", "interfaces"], capture_output=True, text=True)
        output_lines = result.stdout.split('\n')
        for line in output_lines:
            if "SSID" in line:
                return line.split(":")[1].strip()
            
            
    def on_select_port(self, event):
        selected_port = self.listbox.curselection()
        if selected_port:
            target_port_str = self.listbox.get(selected_port)
            target_port = int(target_port_str.split()[1])  # Convert the port number to an integer
            print("Selected Port:", target_port)
            self.gui.destroy()
            from PortDetails import receive_target
            receive_target(target_port)

        
    def init_gui(self):
        # ===== START OF GRAPHICAL USER INTERFACE =====
        self.gui = Tk()
        self.gui.title('Netshield Port')
        self.gui.geometry("400x630+20+20")

        # Colour Palette
        m1c = '#0a0a0a'
        bgc = '#F0FFF0'
        fgc = '#111111'

        self.gui.tk_setPalette(background=bgc, foreground=m1c, activeBackground=fgc, activeForeground=bgc,
                               highlightColor=m1c, highlightBackground=m1c)

        # Page Title
        self.L11 = Label(self.gui, text="Scan Open Port", font=("Helvetica", 16))
        self.L11.place(x=115, y=10)

        # Get IP Address
        self.L21 = Label(self.gui, text="IP Address: ")
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
        self.L26.place(x=16, y=210)
        self.L27 = Label(self.gui)
        self.L27.place(x=200, y=210)

        # Display start time of the scan
        self.L28 = Label(self.gui, text="Search Start Time:")
        self.L28.place(x=16, y=240)
        self.L29 = Label(self.gui, text="")
        self.L29.place(x=180, y=240)

        # Display end time of the scan
        self.L30 = Label(self.gui, text="Search End Time:")
        self.L30.place(x=16, y=270)
        self.L31 = Label(self.gui, text="")
        self.L31.place(x=180, y=270)

        # Display the run time of the scan
        self.L32 = Label(self.gui, text="Search Duration:")
        self.L32.place(x=16, y=300)
        self.L33 = Label(self.gui, text="")
        self.L33.place(x=180, y=300)

        # Display the list of open ports
        self.L34 = Label(self.gui, text="List of Open Ports:")
        self.L34.place(x=16, y=330)
        frame = Frame(self.gui)
        frame.place(x=16, y=360, width=370, height=200)
        self.listbox = Listbox(frame, width=59, height=12)
        self.listbox.pack(expand=YES, fill=BOTH)
        self.listbox.place(x=0, y=0)
        
        # Bind the on_select_port function to the listbox selection event
        self.listbox.bind('<<ListboxSelect>>', self.on_select_port)
    
        scrollbar = Scrollbar(frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        wifi_name = self.get_wifi_name()
        self.L35 = Label(self.gui, text="Network Connected: " + wifi_name)
        self.L35.place(x=20, y=600)
        
        self.L36 = Label(self.gui, text="**You may specify the port range to scan.")
        self.L36.place(x=16, y=115)
        
        self.L36 = Label(self.gui, text="Scan Summary", font=("Helvetica", 14))
        self.L36.place(x=125, y=170)

        # Button for start scan
        self.B11 = Button(self.gui, text="Start Scan", command=lambda: self.start_scan())
        self.B11.place(x=160, y=140, width=70)

        # ==== Start GUI ====
        self.gui.resizable(False, False)
        self.gui.mainloop()
            
scanner = None

def receive_target(target_ip):
    global scanner
    print(f"Target IP: {target_ip}")
    scanner = NetshieldPortScanner(target_ip)
    
