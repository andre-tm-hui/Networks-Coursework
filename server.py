# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 17:06:37 2018

@author: andre
"""
import socket
import time
import sys


def read(filename):     # Function to read in worst100.txt and convert into a nested list
    f = open(filename + ".txt", "r")
    cont = f.readlines()
    
    mp = []
    for x in range(0,len(cont)):
        line = cont[x]
        song = []
        if line[0].isdigit():   # Look for lines that start with a digit; if it does, then a song is on the same line
            atName = False
            i = 1
            while atName == False:      # Iterate through characters until you reach the first character of the name
                if line[i] == "-":
                    i += 1
                    if line[i] == " ":
                        i += 1
                    atName = True
                else:
                    i += 1
            
            name = ""
            author = ""
            nameFin = False
            atAuthor = False
            authorFin = False
            while nameFin == False:     # Iterate through the characters of the name until you reach a blank space/end of line
                name += line[i]
                i += 1
                if i == len(line):      # Check if the you're at the end of line; if true, then you have reached the end of the song name
                    line = cont[x+1]    # Since end of name is end of line, artist name is contained in the next line
                    nameFin = True
                    name = name[0:len(name)-1]
                    song.append(name)
                    i = 0
                elif (line[i] == " ") and (line[i+1] == " "):
                    nameFin = True
                    if len(name) > 31:      # Check if name is longer than 31 characters; if so, the song name has cut into the artist name, and needs to be split
                        author = name[31:]
                        name = name[0:31]
                        atAuthor = True
                        authorFin = True
                        song.append(name)
                        song.append(author)
                    else:
                        song.append(name)
            
            while atAuthor == False:        # Iterate through blank spaces until you reach the first character of the author
                i += 1
                if line[i] != " ":
                    atAuthor = True
                
            while authorFin == False:       # Iterate through characters of artist name until you reach consecutive blank spaces
                author += line[i]
                i += 1
                if (line[i] == " ") and (line[i+1] == " "):
                    authorFin = True
                    song.append(author)
            
        if len(song) != 0:      # Add song to list of songs
            mp.append(song)
            
    return mp


def runServer():    # Main server function
    songList = read("100worst")
    host = '127.0.0.1'
    port = 8000
    
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:    # Initial try to check if port is in use
            s.bind((host, port))
            s.listen()
            s.close
        except:
            consoleOut("Port is in use. Try again later.")
            return
        
    log("\n\n" + getTime() + ' - Server Started\n\n')
    consoleOut('Server Online')
    
    while True:     # Server runs indefinitely, despite any raised exceptions, unless prompted/forced to shutdown
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:    # Main try function, to catch keyboardInterrupt and others
                s.bind((host, port))
                s.listen()
                while True:     # Continue to wait for more clients unless prompted
                    conn, addr = s.accept()
                    with conn:
                        consoleOut(str(addr) + ' Connected')
                        start = time.localtime()
                        elapsed = - time.time()
                        tConnect = getTime()
                        log(getTime() + ' - ' + str(addr) + ' Connected\n')
                        
                        data = conn.recv(1024)  # 2 lines to recieve and send a response to client, to notify the server is ready
                        conn.sendall(data)

                        data = conn.recv(1024)
                        artist = data.decode()
                        if artist != 'quit':    # If client sends disconnect/quit message, don't do a search
                            songs = []
                            for song in songList:
                                if song[1].lower() == artist.lower():
                                    songs.append(song)
                                elif artist.lower() in song[1].lower():
                                    songs.append(song)
                            if len(songs) > 0:
                                output = 'List of songs by ' + artist + ':\n'
                                for song in songs:
                                    output += song[1] + ' - ' + song[0] + '\n'
                                conn.sendall(str.encode(output))
                            else:
                                conn.sendall(str.encode('No songs found for input \'' + artist + '\'.'))
                            data = conn.recv(1024)
                            log('Search Query: ' + artist + '\n')
                        consoleOut(str(addr) + ' Disconnected')
                        elapsed += time.time()
                        log(getTime() + ' - ' + str(addr) + ' Disconnected\n' + str(addr) + ' was connected for ' + str(elapsed) + ' seconds.\n\n')
            except KeyboardInterrupt:   # Shutdown/escape exception
                s.close()
                consoleOut('Server Shutting Down')
                log(getTime() + ' - Server Shutting Down\n\n')
                return
            except:     # Response when more than 2 clients connect at once, or if the client suddenly disconnects
                log('Connection Failed - Client can\'t be reached\n\n')
                consoleOut('Connection Failed - Client can\'t be reached')

def log(s):     # Write s to server.log
    f = open('server.log', 'a+')
    f.write(s)
    f.close()
    return

def consoleOut(s):      # Write s to console/terminal
    print(s)
    sys.stdout.flush()
    return

def getTime():      # Convert time to string
    a = time.localtime()
    t = str(a[0]) + '/' + str(a[1]) + '/' + str(a[2]) + ' - ' + str(a[3]) + ':' + str(a[4]) + ':' + str(a[5])
    return t

def main():
    print('Exit using Ctrl+C. If server does not exit immediately, it will exit on the next client connection.')
    sys.stdout.flush()
    runServer()
    return

main()

