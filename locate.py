from socket import gethostbyname, gethostname
from os import system, _exit
from pyperclip import copy
from requests import get
from asyncio import run, sleep
from json import loads
import fire

IP_INFO_API = "https://ipinfo.io/{0}/json"
PUBLIC_IP_API = "http://checkip.dyndns.com/"

class IP:
    def locate(e, ip: str):
        request = get(IP_INFO_API.format(ip))
        if request.status_code == 200:
            content = loads(request.content.decode('utf-8'))
            print(f"""
IP: {content["ip"]}
Hostname: {content["hostname"]}
Country: {content["country"]}
Region: {content["region"]}
City: {content["city"]}
Aproximated Location: https://www.google.com/maps/search/?api=1&query={content["loc"]}
""")
        elif request.status_code == 400 or request.status_code == 404:
            print("Couldn't find the requested ip info, please review it and try again.")
        else:
            print(f"There is an error connecting to the api. Please try again\nStatus code: {request.status_code}")
            
    def local(e):
        local_ip = gethostbyname(gethostname())
        copy(local_ip)
        print(f"Your local IP Address is: {local_ip}")
        
    def public(e):
        request = get(url=PUBLIC_IP_API)
        if request.status_code == 200:
            content = request.content
            decoded_content = content.decode("utf-8")
            ip = decoded_content.replace("<html><head><title>Current IP Check</title></head><body>Current IP Address: ", "").replace("</body></html>\r\n", "")
            copy(ip)
            print(f"Your public IP is {ip}")
        else: 
            print(f"Couldn't get public IP, status code: {request.status_code}")
            
if __name__ == "__main__":
    fire.Fire(IP)