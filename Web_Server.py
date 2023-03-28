# import socket module for socket programming
from socket import *

# define buffer size and port number
BUFSIZE = 1024
PORT = 8080

def parserequest(msg):
    print("----- Request Message -----")
    print(msg) # print raw request message

    header = msg.split("\n")[0] # split msg by “\n” and put splitedElement[0] in header
    url = header.split()[1] # split header by “ “ and put splitedElement[1] in url
    val = url.split('/') # split url by “/”
    if len(val) < 4: return None; # if the number of url parameters is too small, return None 

    # calculate the values
    if val[2] == '+': return int(val[1]) + int(val[3])
    elif val[2] == '-': return int(val[1]) - int(val[3])
    elif val[2] == '*': return int(val[1]) * int(val[3])
    else: return int(val[1]) / int(val[3])
def main():
    # Make a socket to connect to web browser
    listen_sock = socket(AF_INET, SOCK_STREAM) # using TCP protocol
    listen_sock.bind(('', PORT)) # localhost
    listen_sock.listen(1) 

    while 1:
	#Return new socket for communication to web browser if browser connects
        conn, addr = listen_sock.accept()
        
        print("Client Address : ", addr)

	# Receive request message from web browser
        data = conn.recv(BUFSIZE).decode("UTF-8")
      
 	# parse the request message
        rslt = parserequest(data)
        if (rslt == None):
            rslt = 0

	# Make a HTTP response message to send to the web browser
        msg = "HTTP/1.1 200 OK\r\n\n<html><body>Calculation Results: %d</body></html>" % rslt
        
        conn.sendall(msg.encode("UTF-8")) #Send the response message
        conn.close()
      
main() # execute main method
