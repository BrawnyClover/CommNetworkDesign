import sys
import os
import stat
import copy
import socket as s
import dns.resolver  # module for DNS
from bs4 import BeautifulSoup  # module for html parsing

# define
HTTP_PORT = 80
BUF_SIZ = 1024
LARGE_BUF_SIZ = 20480


# 1. Funciton to make a socket to connect to the server

def MakeSocket(webAddress, portNumber):
    try:
        sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    except OSError:
        print("Socket Error")
        return None
    try:
        sock.connect((webAddress, portNumber))
    except OSError:
        print("Connection Error")
        return None
    return sock


# 2-3. Funtion to make/send a HTTP request message

def SendGetReq(sock, HostName, ObjectName):
    GetReq = "GET %s HTTP/1.1\r\nAccept: */*\r\nHost: %s:%d\r\nConnection: close\r\n\r\n" % (ObjectName, HostName, HTTP_PORT)
    # Make HTTP GET message

    try:
        sock.send(GetReq.encode())  # Send HTTP GET message
    except OSError:
        print("Send Error")
        return False

    return True


# 4. Function to receive the index.html from the server

def RecvResponse(sock, FileName, HostName):
    with open(FileName, "wb") as html:  # Open the file to save the raw http header and object
        os.chmod(FileName, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH)
        # Change the permission from "execute only" to "read, write, execute"

        buf = sock.recv(BUF_SIZ)
        if len(buf) < 0:
            print("Receive Error")
            return

        Temp = copy.deepcopy(buf.decode())  # Copy buf to Temp to print out http header
        pos = Temp.find("\r\n\r\n")
        Temp = Temp[:pos]

        # to print out only http header without objects
        print("=============header=============")
        print("%s" % Temp)

        while True:
            html.write(buf)
            buf = sock.recv(BUF_SIZ)
            if len(buf) == 0: break
            # Receive and save the http object on files


# 5. Function to extracts the header and objects information
def ParseObject(Filename):  # return hostlist, objectlist, count of objects
    with open(Filename, "rb") as html:
        soup = BeautifulSoup(html, 'html.parser')
        taglist = soup.find_all(True)  # find link tags
        hostlist = []
        objlist = []
        cnt = 0

        for tag in taglist:
            if tag.has_attr('src') and tag['src'].find('http://') != -1:
                stripped_tag = tag['src'][7:]
                obj_pos = stripped_tag.find('/')
                hostlist.append(stripped_tag[:obj_pos])
                objlist.append(stripped_tag[obj_pos:])
                cnt += 1
            if tag.has_attr('href') and tag['href'].find('http://') != -1:
                stripped_tag = tag['href'][7:]
                obj_pos = stripped_tag.find('/')
                hostlist.append(stripped_tag[:obj_pos])
                objlist.append(stripped_tag[obj_pos:])
                cnt += 1
    return hostlist, objlist, cnt


# Function to manage the whole process for web browser socket
def RunHTTPInteraction(webAddress):
    fileid = 1
    sock = MakeSocket(webAddress, HTTP_PORT)
    if sock == None:
        return;
    # 1. Make a socket to connect to the server

    FileName = "%d.html" % fileid
    if SendGetReq(sock, webAddress, "/"):
        # 2 - 3. Make and send a HTTP request message to get the index.html
        RecvResponse(sock, FileName, webAddress);  # 4. Receive the index.html from the server
        sock.close()
    else:
        sock.close()
        return
    hostAddress, objectName, objectCounter = ParseObject(FileName);
    # 5. Extracts the header and objects information
    if objectCounter <= 0: return;
    print("=============objects=============")
    print(" the number of objects : %d" % objectCounter)

    for i in range(objectCounter):
        print("host : %s, object : %s" % (hostAddress[i], objectName[i]))


# Print out extracted objects

# main function
domain_name = input("Input URL : ")
DnsResolver = dns.resolver.Resolver()

DnsResolver.nameserver = ['8.8.8.8']  # google

print(DnsResolver.resolve(domain_name).response)
ip_addr = input("Write the received IP address from DNS Server : ")

# Make an HTTP request to the web server using the IP address

RunHTTPInteraction(ip_addr)
