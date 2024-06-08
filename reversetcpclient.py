import socket
import sys
import random

#serverIP='192.168.228.132'
#serverPort=12000
serverIP=sys.argv[1]
serverPort=int(sys.argv[2])
clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientSocket.connect((serverIP, serverPort))
list1=[]

def send_Initialization(n):     #发送Initialization报文
    initialization=f"1,{n}"
    clientSocket.sendall(initialization.encode('utf-8'))   
    print(f"发送Initialization报文,块数为{n}")

def receive_agree():        #接收agree报文
    data = clientSocket.recv(2048)
    try:
        agreedata=data.decode('utf-8')
        if agreedata=="2":
            return True
    except Exception as e:  
        print("ERROR:", e)
    return False

def send_reverseRequest(lens,data):     #发送reverseRequest
    reverseRequest=f"3,{lens},{data}"
    clientSocket.sendall(reverseRequest.encode('utf-8'))

def receive_reverseAnswer(i):       #接收receive_reverseAnswer
    data = clientSocket.recv(2048)  
    try:
        answerdata=data.decode('utf-8')
        answerdata=answerdata.split(",")
        if answerdata[0]=="4":
            print(i,"：",answerdata[2])
            return True
    except Exception as e:  
        print("ERROR:", e)
    return False

minL=int(sys.argv[3])
maxL=int(sys.argv[4])
#minL=10
#maxL=20

#读取文件内容
with open("temp.txt",'r',encoding='utf-8') as file:
    content=file.read()
n=random.randint(3,10)  #随机生成块数n
for i in range(n):      #获取随机文本
    start = random.randint(0, len(content) - maxL)
    end=start+random.randint(minL,maxL)
    ss=content[start:end]
    list1.append(ss);   

send_Initialization(n)      #发送Initialization报文
flag=receive_agree()        #接收agree报文
while flag:         #发送reverseRequest
    for i in range(n):
        send_reverseRequest(len(list1[i]),list1[i])
        receive_reverseAnswer(i+1)
    flag=False
clientSocket.close()
print("关闭套接字")

# 反转内容并写入新的文件夹
reversed_content = content[::-1]  
with open("temp_new.txt", 'w', encoding='utf-8') as file:  
    file.write(reversed_content)

