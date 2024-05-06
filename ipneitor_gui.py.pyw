from customtkinter import CTkButton as Button
from customtkinter import CTkFrame as Frame
from customtkinter import CTkLabel as Label
from customtkinter import CTkEntry as Entry
from customtkinter import CTk 
from customtkinter import CTkFont as Font
from pyperclip import copy
from requests import get
from socket import gethostbyname, gethostname
from tkinter import StringVar, Menu
from tkinter import messagebox
from asyncio import run
from os import _exit
from json import loads

TITLE = "IPneitor GUI Edition - By: 0.1fps on discord"
PUBLIC_IP_API = "http://checkip.dyndns.com/"
IP_INFO_API = "https://ipinfo.io/{0}/json"

class Window(CTk):
    def __init__(self):
        # Window config
        super().__init__()
        self.title(TITLE)
        self.geometry("720x480")
        
        #Menu
        get_ip_menu = Menu(self, tearoff=0)
        get_ip_menu.add_command(label="Local IP", command= lambda: run(self.get_private_ip()))
        get_ip_menu.add_command(label="Public IP", command= lambda: run(self.get_public_ip()))
        
        self.nav_bar = Menu(self)
        self.nav_bar.add_cascade(label="Get IP", menu=get_ip_menu)
        self.nav_bar.add_command(label="Exit", command=lambda: _exit(0))
        
        self.config(menu=self.nav_bar)
        
        #Title
        self.title = StringVar(value="IPneitor Tool")
        self.title_label = Label(self, 
                                 textvariable=self.title, 
                                 font=Font(family="Calibri",
                                                            weight="bold",
                                                            size=26))
        self.title_label.pack()
        
        #GUI
        self.ip = Entry(self, placeholder_text="IP")
        self.output = StringVar(value="")
        self.out_label = Label(self, 
                               textvariable=self.output,
                               font=Font(family="Calibri",
                                         size=18))
                               

        self.out_label.bind("<Button-1>", lambda event: copy(self.output.get()))
        
        self.ip.pack()
        self.out_label.pack(side="left")
        
        self.bind('<Return>', func=lambda event: run(self.get_ip_info(self.ip.get())))
    
    #IP info function
    async def get_ip_info(self, ip: str):
        request = get(IP_INFO_API.format(ip))
        try: 
            if request.status_code == 200:
                content = loads(request.content.decode('utf-8'))
                self.output.set(f"""
IP: {content["ip"]}                                                                   
Hostname: {content["hostname"]}                                                       
Country: {content["country"]}                                                         
Region: {content["region"]}                                                           
City: {content["city"]}                                                               
Aproximated Location: https://www.google.com/maps/search/?api=1&query={content["loc"]}
""")
            elif request.status_code == 400 or request.status_code == 404:
                messagebox.showerror("Error","Couldn't find the requested ip info, please review it and try again.")
            else:
                messagebox.showerror("Error",f"There is an error connecting to the api. Please try again\nStatus code: {request.status_code}")
        except:
            messagebox.showerror("Error",f"There is an error connecting to the api. Please check the ip\nStatus code: {request.status_code}")
    
    #Private IP function
    async def get_private_ip(self):
        local_ip = gethostbyname(gethostname())
        copy(local_ip)
        messagebox.showinfo("Done!", "Your local ip has been copied to your clipboard!")
        
    # Public IP function
    async def get_public_ip(self):
        request = get(url=PUBLIC_IP_API)
        if request.status_code == 200:
            content = request.content
            decoded_content = content.decode("utf-8")
            ip = decoded_content.replace("<html><head><title>Current IP Check</title></head><body>Current IP Address: ", "").replace("</body></html>\r\n", "")
            copy(ip)
            messagebox.showinfo("Done!", "Your public ip has been copied to your clipboard!")
        else: 
            messagebox.showerror("Error", f"Couldn't get public IP, status code: {request.status_code}")
        
        
# Starting the window
root = Window().mainloop()