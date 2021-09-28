# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 14:52:18 2018

@author: andre
"""

import socket
import time
import sys

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 8000        # The port used by the server
socket.setdefaulttimeout(5) # Set program to timeout/raise an exception after 5 seconds

def query():    # Main Function
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        
        try:    # Initial try statement to check if the server is online
            s.connect((HOST, PORT))
        except Exception as e:
            consoleOut('Could not connect, server is not online.')
            return
        s.sendall(str.encode('check'))
        
        try:    # Second try statement to check if server is busy
            
            data = s.recv(1024)
        except:
            s.close()
            consoleOut('Server is busy. Try again Later.')
            return

        socket.setdefaulttimeout(100) # Reset timeout
        try:    # Third try statement to catch any exceptions during the running of the search
            artist = input('Search for an artist: ')
            while artist == "":     # Ensure that a name is entered
                artist = input('Please enter an artist: ')
            elapsed = - (time.time()*1000)
            s.sendall(str.encode(artist))
            data = s.recv(1024)
            elapsed += (time.time()*1000)
            nBytes = sys.getsizeof(data)

            log(getTime() + ' - Received server response (' + str(elapsed) + 'ms elapsed).\nQuery: ' + artist + '\nSize of response is ' + str(nBytes) + ' bytes.\n\n')
                    
            consoleOut(data.decode())
            input('Press Enter to exit.')
            s.sendall(b'')
            s.close()
            consoleOut('Disconnected.')
        except KeyboardInterrupt:   # Catch Ctrl+C to quit search midway
            consoleOut('Disconnecting.')
            s.sendall(str.encode('quit'))   # Tell the server to disconnect
            s.close()
        except:     # Catch exception in case server randomly crashes/shuts down during search
            consoleOut('Cannot reach server. Try again Later.')
    return

def log(s):     # Write s to client.log
    f = open('client.log', 'a+')
    f.write(s)
    f.close()
    return

def consoleOut(s):      # Write s to console/terminal
    print(s)
    sys.stdout.flush()
    return

def getTime():  # Function to turn current time to a string for logs
    a = time.localtime()
    t = str(a[0]) + '/' + str(a[1]) + '/' + str(a[2]) + ' - ' + str(a[3]) + ':' + str(a[4]) + ':' + str(a[5])
    return t

def main():
    query()
    return

main()


