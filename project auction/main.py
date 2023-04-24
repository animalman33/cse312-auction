import socketserver


class TPChandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(2048)
        data2 = data.split("\r\n\r\n".encode())
        data3=data2[0].split("\r\n".encode())
        data4=data3[0].split(" ".encode())
        #print(data2)
        if data4[0] == "GET".encode():
            if data4[1] == "/".encode():
                    with open("website/index.html", "rb") as i:
                        i = i.read()
                    self.request.sendall((f"HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length:{len(i)}\r\n\r\n").encode() + i)
            elif data4[1] == "/login".encode():
                    with open("website/index.html", "rb") as i:
                         i = i.read()
                    self.request.sendall((f"HTTP/1.1 301 Moved Permanently\r\nContent-Length: {len(i)}\r\nLocation:/\r\n\r\n").encode()+i)

            elif data4[1] == "/style.css".encode():
                   with open("website/style.css", "rb") as i:
                      i = i.read()
                   self.request.sendall((f"HTTP/1.1 200 OK\r\nContent-Type: text/css; charset=utf-8\r\nX-Content-Type-Options: nosniff\r\nContent-Length:{len(i)}\r\n\r\n").encode() + i)
            elif data4[1] == "/functions.js".encode():
                with open("website/functions.js", "rb") as i:
                    i = i.read()
                self.request.sendall((f"HTTP/1.1 200 OK\r\nContent-Type: text/javascript; charset=utf-8\r\nX-Content-Type-Options: nosniff\r\nContent-Length:{len(i)}\r\n\r\n").encode() + i)

        elif data4[0] == "POST".encode():
            z = data
            bound = (z.split("boundary=----".encode(), 1))[1].split("\r\n".encode(), 1)[0]
            boundary = "------".encode() + bound
            if data4[1] == "/login".encode():
                print("do login stuff")
                with open("website/index.html", "rb") as i:
                    i = i.read()
                self.request.sendall((f"HTTP/1.1 301 Moved Permanently\r\nContent-Length: {len(i)}\r\nLocation:/\r\n\r\n").encode() + i)
            if data4[1] == "/register".encode():
                print("do register stuff")
                with open("website/index.html", "rb") as i:
                    i = i.read()
                self.request.sendall(
                    (f"HTTP/1.1 301 Moved Permanently\r\nContent-Length: {len(i)}\r\nLocation:/\r\n\r\n").encode() + i)



if __name__ == '__main__':
   host = "0.0.0.0"
   port = 8000
   server = socketserver.ThreadingTCPServer((host, port), TPChandler)
   server.serve_forever()
    # docker-compose up --build --force-recreate
   #docker-compose restart
   #docker-compose up
