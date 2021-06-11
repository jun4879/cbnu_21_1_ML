import socket
import json

# chatbot engine connection info
host = "127.0.0.1"
port = 5050

# client program start
while True:
    print("종료하려면 exit 입력")
    query = input("질문 : ")
    if query == "exit":
        exit(0)
    print("-"*40)

    # chatbot engine server connect
    mySocket = socket.socket()
    mySocket.connect((host, port))

    # chatbot engine query request
    json_data = {'Query': query, 'BotType': "MyService"}
    message = json.dumps(json_data)
    mySocket.send(message.encode())

    # chatbot engine answer print
    data = mySocket.recv(2048).decode()
    ret_data = json.loads(data) # json type string을 json 객체로 변환
    print("답변 : ")
    print(ret_data['Answer'])
    print("\n")

mySocket.close()
