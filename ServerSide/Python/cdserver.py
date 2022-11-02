# -*- coding: utf-8 -*-
import socket
import os
import time
import sys

while True:
    SERVER_HOST = "0.0.0.0"
    SERVER_PORT = 5008

    BUFFER_SIZE = 4096

    s = ''

    # create a socket object
    s = socket.socket()

    # bind the socket to all IP addresses of this host
    try:
        s.bind((SERVER_HOST, SERVER_PORT))
    except OSError:
        print('binding used. Waiting client program exiting')
        s.bind((SERVER_HOST, 9595))
        s.close()
        continue

    # make the PORT reusable
    # when you run the server multiple times in Linux, Address already in use error will raise
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.listen(5)
    print(f"Listening as {SERVER_HOST}:{SERVER_PORT} ...")

    # accept any connections attempted
    client_socket, client_address = s.accept()
    print(f"{client_address[0]}:{client_address[1]} Connected!")

    # just sending a message, for demonstration purposes
    message = "Hello and Welcome".encode()
    client_socket.send(message)

    # get STAmac
    print("Getting MAC Address..")
    command = 'type macAddress.txt'
    client_socket.send(command.encode())
    results = client_socket.recv(BUFFER_SIZE).decode()
    results = results.replace('-', ':')
    print(results)
    f = open("STAmac.txt", 'w')
    f.write(results)
    f.close()
    am = results
    print("mac accept :" + am)

    # get AdaptName
    print('Getting Adapt Name...')
    command = 'type adaptName.txt'
    client_socket.send(command.encode())
    results = client_socket.recv(BUFFER_SIZE).decode()
    f = open("adaptName.txt", 'w')
    f.write(results)
    f.close()
    an = results
    print("adaptName accept" + an)

    client_socket.settimeout(2)

    # session cnt, client session out
    s_cnt = 0
    cso = 0
    # cnt = 0
    while True:
        # get the command from prompt
        # command = input("Enter the command you wanna execute:")
        #data, address = s.recv(client_socket, BUFFER_SIZE)

        print("Waiting Command Line...")

        time.sleep(1)
        f = open("isAuth.txt", 'r')
        line = f.readline()
        print('isAuth : ' + line)
        line = int(line)
        f.close()

        # session check
        while True:
            print('test1')
            MESSAGE = "Hello, World!"
            print('test1.5')
            try:
                client_socket.send(MESSAGE.encode())
                print('test1.6')
                print(client_socket.gettimeout())
                # client_socket.timeout
                results = client_socket.recv(BUFFER_SIZE).decode()
                if(results):
                    break
                print(results)
                print('test2')
            except:
                print("client session out")
                cso = 1
                client_socket.close()
                # close server connection
                # s.close()
                s = 'asd'
                break

        if(cso == 1):
            cso = 0
            break

        os.system('/sbin/wifi reload wlan1')
        time.sleep(2)
        if(line == 1):
            print(line)
            print("Authed")

            # toss ssidName
            command = 'pscp -scp -r -pw 1 root@192.168.2.1:/mnt/sda1/test/ssidName.txt ./'
            # send the command to the client
            client_socket.send(command.encode())
            results = client_socket.recv(BUFFER_SIZE).decode()
            # print them
            print(results)

            # toss wifi.py
            command = 'pscp -scp -r -pw 1 root@192.168.2.1:/mnt/sda1/test/wifi.py ./'
            # send the command to the client
            client_socket.send(command.encode())
            if command.lower() == "exit":
                # if the command is exit, just break out of the loop
                break
            # retrieve command results
            results = client_socket.recv(BUFFER_SIZE).decode()
            # print them
            print(results)
            time.sleep(2)
            command = 'python wifi.py'
            # send the command to the client
            client_socket.send(command.encode())
            if command.lower() == "exit":
                # if the command is exit, just break out of the loop
                break
            # retrieve command results
            try:
                results = client_socket.recv(BUFFER_SIZE).decode()

            except:
                print("QDQD timeout")
                break

            # print them
            print(results)

            f = open("isAuth.txt", 'w')
            f.write("0")
            print("test1\n")
            f.close()
            print("test2\n")

            print("test3\n")

            # command = 'exit'
            # # send the command to the client
            # client_socket.send(command.encode())

            break

        else:
            # print(line)
            print("Not Auth")

    # close connection to the client
    client_socket.close()
    # close server connection
    try:
        s.close()
    except:
        s = 'asd'

    print("finish")
    s = ''
    time.sleep(3)
