from flask import Flask, request, jsonify, abort
import socket
import json

# 챗봇 엔진 접속 정보
host = "127.0.0.1"
port = 5050
app = Flask(__name__)


def get_answer_from_engine(bottype, query):
    # 챗봇 엔진 서버 연결
    mySocket = socket.socket()
    mySocket.connect((host, port))

    # 챗봇 엔진 질의 요청
    json_data = {'Query': query, 'BotType': bottype}
    message = json.dumps(json_data)
    mySocket.send(message.encode())

    # 챗봇 엔진 답변 출력
    data = mySocket.recv(2048).decode()
    ret_data = json.loads(data)

    # 챗봇 엔진 서버 연결 소켓 닫기
    mySocket.close()

    return ret_data

# 챗봇 엔진 query 전송 api
@app.route('/query/<bot_type>', method=['POST'])
def query(bot_type):
    body = request.get_json()

    try:
        if bot_type == 'TEST':
            # 챗봇 api test
            ret = get_answer_from_engine(bottype=bot_type, query=body['query'])
            return jsonify(ret)

        elif bot_type == 'KAKAO':
            pass

        elif bot_type == 'NAVER':
            pass

        else :
            abort(404)

    except Exception as ex:
        print(ex)
        abort(500)  # 오류 발생 시 500 오류


if __name__ == '__main__':
    app.run()
