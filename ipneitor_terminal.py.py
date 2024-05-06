from socket import gethostbyname, gethostname
from os import system, _exit
from pyperclip import copy
from requests import get
from asyncio import run, sleep
from json import loads

PUBLIC_IP_API = "http://checkip.dyndns.com/"
IP_INFO_API = "https://ipinfo.io/{0}/json"
HELP_MESSAGE = """
IPneitor commands

Local (alias: l): Prints and copy the current local IP address
Public (alias: p): Prints and copy the current public IP address
Info (alias: i): Prints all the information about the IP provided

Exit: Close the program
"""

system("title IPneitor By: Masterrecording")
system("color a")


async def get_public_ip():
    request = get(url=PUBLIC_IP_API)
    if request.status_code == 200:
        content = request.content
        decoded_content = content.decode("utf-8")
        ip = decoded_content.replace("<html><head><title>Current IP Check</title></head><body>Current IP Address: ", "").replace("</body></html>\r\n", "")
        copy(ip)
        print(f"Your public IP is {ip}")
    else: 
        print(f"Couldn't get public IP, status code: {request.status_code}")


async def get_private_ip():
    local_ip = gethostbyname(gethostname())
    copy(local_ip)
    print(f"Your local IP Address is: {local_ip}")
    

async def get_ip_info(ip: str | None = None):
    if ip == None: ip = input("Please provide the IP\n>")
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
    
    
async def main():
    print(HELP_MESSAGE)
    while True:
        match input("> ").lower():
            case "local":
                await get_private_ip()
            case "l":
                await get_private_ip()
            case "public":
                await get_public_ip()
            case "p":
                await get_public_ip()
            case "info":
                await get_ip_info()
                await sleep(1)
            case "i":
                await get_ip_info()
                await sleep(1)
            case "exit":
                _exit(0)
            case "e":
                _exit(0)
            case _:
                print(HELP_MESSAGE)
        
    
run(main())