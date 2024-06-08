import socket    
  
serverPort = 12000    
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
serverSocket.bind(('', serverPort))  
serverSocket.listen(10)  
print("THE SERVER IS READY TO RECEIVE")  
  
def receive(client):  
    try:  
        data = client.recv(2048)  
        initialization = data.decode('utf-8')
        initialization=initialization.split(",")
        if initialization[0] == "1":
            agree = f"2"
            client.sendall(agree.encode('utf-8'))
            n=int(initialization[1])
            for i in range(1,n+1):
                data_r = client.recv(2048)  
                reverseR =data_r.decode('utf-8')
                reverseR=reverseR.split(",")
                if reverseR[0] == "3":  
                    ss = reverseR[2]  
                    rs = ss[::-1]  
                    reverseAnswer = f"4,{len(rs)},{rs}"    
                    client.sendall(reverseAnswer.encode('utf-8'))  
  
    except Exception as e:  
        print("ERROR:", e)  
    finally:
        client.close()
        print("断开连接")
  
while True:  
    client, clientaddr = serverSocket.accept()  
    print(f"Accepted connection from {clientaddr}")  
    receive(client)
    
