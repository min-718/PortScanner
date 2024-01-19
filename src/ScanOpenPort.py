import socket # == sockets allows to establish network connections over various network protocol
import sys
import threading
import time
from tkinter import *
import subprocess

# ==== Scan Vars ====
ip_s = 1 #Default 
ip_f = 1024 
log = [] 
ports = [] # array to store ports
target = 'localhost' #default for ip
start_time = None
end_time = None
open_ports_found = False

# Scan Open Port Function (run in thread)
# This function attempts to connect to a specified port on the target
# If connection successful, it adds the open port information to the log and updates the GUI
def scanPort(target, port):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(4)
		c = s.connect_ex((target, port))
		if c == 0:
			m = ' Port %d ' % (port,)
			ports.append(port)
			listbox.insert("end", str(m)) #append to the end of list
			updateNoOfOpenPort()
			open_ports_found[0] = True #Set to True if open port is found
		s.close()
	except OSError: 
		print('!!!Too many open sockets. Port ' + str(port)+'!!!')
	except:
		c.close()
		s.close()
		sys.exit() 

# This funtion count the number of open port at the IP address
def updateNoOfOpenPort():
	rtext = " [ " + str(len(ports)) + " / " + str(ip_f) + "]"
	L27.configure(text = rtext)

# This function clear the contents in the listbox
def clearScan():
		listbox.delete(0, 'end')


# Initiates the scanning process when the user click the "Start Scan" button
def startScan():
	global ports, log, target, ip_f, start_time, end_time

	clearScan()

	ports = []
	start_time = time.time()
	L29.configure(text=time.strftime("%Y-%m-%d %H:%M:%S"))

	# Get ports ranges from GUI (get the starting point and ending point of ports)
	ip_s = int(L24.get())
	ip_f = int(L25.get())

	open_ports_found = False
	
	# Retrieve the target IP address from the GUI input
	target = socket.gethostbyname(str(L22.get()))

	# Initiates a loop to scan the ports in the specific IP
	while ip_s <= ip_f:
			try:
				scan = threading.Thread(target=scanPort, args=(target, ip_s))
				scan.setDaemon(True)
				# start the thread
				scan.start()
			except: time.sleep(0.01)
			# Increment of the port number
			ip_s += 1
	
	end_time = time.time()
	runtime = end_time - start_time
	L31.configure(text=time.strftime("%Y-%m-%d %H:%M:%S"))
	L33.configure(text=f"{runtime:.2f} seconds")
	log.append(" End Time:\t" + time.strftime("%Y-%m-%d %H:%M:%S"))
	log.append(" Runtime:\t{:.2f} seconds".format(runtime))

	if not open_ports_found:
		listbox.insert("end", "No open ports found on IP Address {}".format(target))
		
# Get the network connected
def get_wifi_name():
    result = subprocess.run(["netsh", "wlan", "show", "interfaces"], capture_output=True, text=True)
    output_lines = result.stdout.split('\n')
    for line in output_lines:
        if "SSID" in line:
            return line.split(":")[1].strip()
		


# ===== START OF GRAPHICAL USER INTERFACE ===== 
gui = Tk()
gui.title('Netshield Port')
gui.geometry("400x600+20+20")

# Colour Palette
m1c = '#0a0a0a'
bgc = '#F0FFF0'
dbg = '#000000'
fgc = '#111111'

gui.tk_setPalette(background=bgc, foreground=m1c, activeBackground=fgc,activeForeground=bgc, highlightColor=m1c, highlightBackground=m1c)

# Page Title
L11 = Label(gui, text = "Scan Summary",  font=("Helvetica", 16))
L11.place(x = 125, y = 10)

# Get IP Address
L21 = Label(gui, text = "IP Address: ")
L21.place(x = 16, y = 60)

L22 = Entry(gui)
L22.place(x = 180, y = 60)

# Get the Port Range (By default 1-1024)
L23 = Label(gui, text = "Ports Range: ")
L23.place(x = 16, y = 90)

L24 = Entry(gui, text = "1")
L24.place(x = 180, y = 90, width = 95)
L24.insert(0, "1")

L25 = Entry(gui, text = "1024")
L25.place(x = 290, y = 90, width = 95)
L25.insert(0, "1024")

# Display number of open ports
L26 = Label(gui, text = "Number of Open Ports: ")
L26.place(x = 16, y = 120)
L27 = Label(gui)
L27.place(x = 200, y = 120)

# Display start time of the scan
L28 = Label(gui, text="Start Time:")
L28.place(x=16, y=150)
L29 = Label(gui, text="")
L29.place(x=180, y=150)

# Display end time of the scan
L30 = Label(gui, text="End Time:")
L30.place(x=16, y=180)
L31 = Label(gui, text="")
L31.place(x=180, y=180)

# Display the run time of the scan
L32 = Label(gui, text="Search Duration:")
L32.place(x=16, y=210)
L33 = Label(gui, text="")
L33.place(x=180, y=210)

# Display the list of open ports
L34 = Label(gui, text="List of Open Ports:")
L34.place(x=16, y=270)
frame = Frame(gui)
frame.place(x = 16, y = 300, width = 370, height = 200)
listbox = Listbox(frame, width = 59, height = 12)
listbox.pack(expand=YES, fill=BOTH)
listbox.place(x = 0, y = 0)
listbox.bind('<<ListboxSelect>>')
scrollbar = Scrollbar(frame)
scrollbar.pack(side=RIGHT, fill=Y)
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

wifi_name = get_wifi_name()
L35 = Label(gui, text="Network Connected: " + wifi_name)
L35.place(x=20, y=570)

# Button for start scan
B11 = Button(gui, text = "Start Scan", command=startScan)
B11.place(x = 16, y = 500, width = 70)

# Button to return to the previous page
B21 = Button(gui, text = "Back")
B21.place(x = 90, y = 500, width = 70)

# Button for download result
B21 = Button(gui, text = "Download Result")
B21.place(x = 210, y = 500, width = 100)

# ==== Start GUI ====
gui.resizable(False, False)
gui.mainloop()
