from tkinter import *
import socket
import ipaddress
import nmap


class NetshieldPortGUI:
    def __init__(self, master):
        self.master = master
        master.title('Netshield Port')
        master.geometry("400x600+20+20")

        # Colour Palette
        self.configure_color_palette()

        # Page Title
        self.create_title_label()

        # Network Information
        self.create_network_labels()

        # Button for discovering hosts
        self.create_discover_hosts_button()

        # Display the list of live hosts
        self.create_live_hosts_widgets()

        # Get the network information and update the labels
        network_info = self.get_network_info()
        if network_info:
            self.update_network_labels(*network_info)

    def configure_color_palette(self):
        m1c = '#0a0a0a'
        bgc = '#F0FFF0'
        fgc = '#111111'
        self.master.tk_setPalette(background=bgc, foreground=m1c, activeBackground=fgc, activeForeground=bgc,
                                  highlightColor=m1c, highlightBackground=m1c)

    def create_title_label(self):
        self.label_title = Label(self.master, text="Netshield Port", font=("Helvetica", 16))
        self.label_title.place(x=125, y=10)

    def create_network_labels(self):
        # Display the network name
        self.label_network_name_title = Label(self.master, text="Connected Network :")
        self.label_network_name_title.place(x=16, y=50)

        self.label_network_name = Label(self.master, text="USMSecure", font=("Helvetica", 10))
        self.label_network_name.place(x=180, y=50)

        # Display the network IP range
        self.label_network_range_title = Label(self.master, text="Network IP Range :")
        self.label_network_range_title.place(x=16, y=75)

        self.label_network_range = Label(self.master, text="", font=("Helvetica", 10))
        self.label_network_range.place(x=180, y=75)

    def create_discover_hosts_button(self):
        self.button_discover_hosts = Button(self.master, text="Discover Hosts", command=self.discover_hosts)
        self.button_discover_hosts.place(x=100, y=140, width=120)

    def create_live_hosts_widgets(self):
        # Display the list of live hosts
        self.label_live_hosts_title = Label(self.master, text="Live Hosts :")
        self.label_live_hosts_title.place(x=16, y=180)

        self.listbox_live_hosts = Listbox(self.master, width=40, height=10)
        self.listbox_live_hosts.place(x=100, y=185)

        self.scrollbar_live_hosts = Scrollbar(self.master, command=self.listbox_live_hosts.yview)
        self.scrollbar_live_hosts.place(x=404, y=300, height=self.listbox_live_hosts.winfo_reqheight())
        self.listbox_live_hosts.config(yscrollcommand=self.scrollbar_live_hosts.set)

    def get_network_info(self):
        try:
            host_name = socket.gethostname()
            host_ip = socket.gethostbyname(host_name)
            network = ipaddress.IPv4Network(f'{host_ip}/24', strict=False)
            return "USMSecure", network
        except Exception as e:
            print(f"Error: {e}")
            return None

    def update_network_labels(self, network_name, network_range):
        self.label_network_name.config(text=network_name)
        self.label_network_range.config(text=str(network_range))

    def discover_hosts(self):
        try:
            network_range = str(self.get_network_info()[1])
            live_hosts = self.discover_hosts_in_range(network_range)

            self.listbox_live_hosts.delete(0, 'end')  # Clear the listbox

            if live_hosts:
                for host in live_hosts:
                    self.listbox_live_hosts.insert(END, host)
            else:
                self.listbox_live_hosts.insert(END, "No live hosts found.")
        except Exception as e:
            print(f"Error: {e}")

    def discover_hosts_in_range(self, ip_range):
        nm = nmap.PortScanner()
        nm.scan(hosts=ip_range, arguments='-sn')

        live_hosts = []
        for host in nm.all_hosts():
            if nm[host]['status']['state'] == 'up':
                live_hosts.append(host)

        return live_hosts


def main():
    root = Tk()
    app = NetshieldPortGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
