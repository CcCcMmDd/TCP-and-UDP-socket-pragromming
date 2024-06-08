
import socket   
from datetime import datetime  
import random

first_server_response_time=datetime.now()

serverPort = 8888  
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#绑定套接字到指定的地址和端口
serverSocket.bind(('', serverPort))  #''表示服务器应该监听来自任何IP地址的连接
  
def send_response(clientAddress, seq):  #发送reponse报文
    curr_time=datetime.now()
    servertime=curr_time.strftime("%H:%M:%S")
    if seq==1:
        global first_server_response_time
        first_server_response_time=curr_time
    total_time=(curr_time-first_server_response_time).total_seconds() * 1000
    total_time=round(total_time,2)
    response=f"{seq},2,{servertime},{total_time}" 
    serverSocket.sendto(response.encode('utf-8'), clientAddress)  
 
  

loss = 0.3  # 30% 的丢包率   
  
while True:    
    try:  
        packet, clientAddress = serverSocket.recvfrom(2048)
        packet=packet.decode()
        if "Connect" in packet:
            print("连接建立") 
            continue
        elif "Disconnect"  in packet:
            print("连接关闭")
            print()
            #break;
        else:
        # 模拟丢包  
            if random.random() > loss:
                packet=packet.split(",")
                #print(packet)
                seq = int(packet[0])     #获取请求的seq
                send_response(clientAddress, seq)  
    except Exception as e:  
        print("ERROR:", e)  
  
