from socket import *

class Server:
    def __init__(self):
        self.BUFSIZE = 1024
        self.PORT = 8080

        self.listen_sock = socket(AF_INET, SOCK_STREAM) # Using TCP protocol
        self.listen_sock.bind(('', self.PORT)) # Localhost
        self.listen_sock.listen(1) 


    def act(self):
        while True:
            conn, addr = self.listen_sock.accept()
            print("Client Address : ", addr)
            data = conn.recv(self.BUFSIZE).decode("UTF-8")

            val = self.parse_request(data)
            result = self.numerical_proc(val)

            if result is None:
                result = 0
            
            ret_msg = f'HTTP/1.1 200 OK\r\n\n<html><body>Calculation Results: {result}</body></html>'

            conn.sendall(ret_msg.encode("UTF-8"))
            conn.close()

    def numerical_proc(self, val):
        if len(val) < 4:
            return None
        
        a, b = int(val[1]), int(val[3])

        if val[2] == '+':
            return a+b
        elif val[2] == '-':
            return a-b
        elif val[2] == '*':
            return a*b
        else:
            return a/b


    def parse_request(self, msg):
        print("----------Request Message---------")
        print(msg)

        header = msg.split("\n")[0]
        url = header.split()[1]
        val = url.split('/')
        return val

if __name__ == "__main__":
    server = Server()
    server.act()