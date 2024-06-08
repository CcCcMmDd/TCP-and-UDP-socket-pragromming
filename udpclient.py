import socket
import time
import sys
from datetime import datetime
import select
import numpy as np
import string
import random

#serverIP='192.168.228.132'
#serverPort=8888
serverIP=sys.argv[1]
serverPort=int(sys.argv[2])
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)#创建套接字UDP
timeout=0.1     #100ms 设置时延
sum_packet_send=0    #发送的总数目
sum_packet_receive=0    #收包的总数目
send_time1=0    #记录第一次发包的时间
total_server_time=0   #server整体响应时间
rtt=0
RTT=[]   #统计rtt的列表

#A~Z,a~z,0~9的列表（用于后续packe的随机消息）
all_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

def send_connect_message():  # 建立连接的消息 
    curr_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
    packet = f"2,Connect,{curr_time}"  # f-string格式化字符串 
    clientSocket.sendto(packet.encode('utf-8'), (serverIP, serverPort))   
    print("发送建立连接请求")  

def send_disconnect_message():  # 断开连接的消息
    curr_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
    packet = f"2,Disconnect,{curr_time}" 
    clientSocket.sendto(packet.encode('utf-8'), (serverIP, serverPort))   
    print("发送断开连接请求")  
  
def send_packet(seq):   #发送数据包
    global sum_packet_send
    global send_time1
    global total_server_time
    if send_time1==0:       #第一次发送数据包的时间
        send_time1=datetime.now()
    curr_time=send_time1.strftime("%Y-%m-%d %H:%M:%S")
    random_chars = ''.join(random.sample(all_chars, 10))
    packet=f"{seq},2,{curr_time}-{random_chars}" 
    clientSocket.sendto(packet.encode('utf-8'), (serverIP, serverPort))
    sum_packet_send+=1
    print("Send squence no ",seq)

      

def receive(seq):   #接收响应
    global sum_packet_receive
    global send_time1
    global total_server_time
    # 使用select模块的非阻塞方式等待数据，超时时间为timeout秒  
    r = select.select([clientSocket], [], [], timeout)
    if r[0]:     #如果收到了数据
        recvdata, addr = clientSocket.recvfrom(2048)
        try:
            recvdata=recvdata.decode()
            if recvdata=="":
                return False
            recvdata=recvdata.split(",")
            if int(recvdata[1])==2 and int(recvdata[0])==seq:
                receive_time=datetime.now()
                total_server_time=recvdata[3]
                rtt = (receive_time - send_time1).total_seconds() * 1000  # 毫秒
                sum_packet_receive+=1
                rtt=round(rtt,2)
                RTT.append(rtt)
                print("Sequence",seq," - IP:",serverIP," - Port:",serverPort," - RTT: ",rtt,"ms - ServerTime:",recvdata[2])
                print()
                send_time1=0
                return True
        except Exception as e:  
            print("ERROR:", e)    
    return False

send_connect_message()

for seq in range(1,13): #12个数据包发出
    send_packet(seq)
    flag=False
    #if seq==5:   time.sleep(5)
    #处理重传
    for i in range(3):  
        if receive(seq):
            flag=True
            break  # 如果收到响应，则跳出重传循环  
        else:
            if i<2:
                print(f"sequence {seq} ，request time out")  
                send_packet(seq)  # 重传数据包  
    if(flag==False):
        # 如果三次尝试都未收到响应，则打印丢包信息  
        print(f"两次重传失败，数据包{seq}丢弃")
        print()

# 发送断开连接的消息  
send_disconnect_message()  
# 关闭socket  
clientSocket.close()
print("连接关闭")
print()

print(f"发送了12个数据包，其中发送的总次数是：{sum_packet_send}")
print(f"收到响应的次数：{sum_packet_receive}")
print(f"最大RTT：{max(RTT)}")
print(f"最小RTT：{min(RTT)}")
print(f"平均RTT：{(sum(RTT)/len(RTT)):.2f}")
print(f"RTT的标准差：{np.std(RTT):.2f}")
loss_rate=1-sum_packet_receive/sum_packet_send
print(f"丢包率为：{(loss_rate*100):.2f}%")
print("Server的整体响应时间：",total_server_time,"ms")
