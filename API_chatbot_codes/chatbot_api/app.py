from flask import Flask, request, jsonify, abort
import socket
import json
from NaverEvent import NaverEvent

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
    print("message: ", message)
    mySocket.send(message.encode())

    # 챗봇 엔진 답변 출력
    data = mySocket.recv(2048).decode()
    ret_data = json.loads(data)

    # 챗봇 엔진 서버 연결 소켓 닫기
    mySocket.close()

    return ret_data


# 챗봇 엔진 query 전송 api
@app.route('/query/<bot_type>', methods=['POST'])
def query(bot_type):
    body = request.get_json()

    try:
        if bot_type == "test":
            # 챗봇 api test
            ret = get_answer_from_engine(bottype=bot_type, query=body['query'])
            return jsonify(ret)

        elif bot_type == "kakao":
            pass

        elif bot_type == "naver":
            body = request.get_json()
            user_key = body['user']
            event = body['event']
            authorization_key = 'VSGpbFkNQaSwVl5oOkmE'
            naverEvent = NaverEvent(authorization_key)

            if event == "open":
                print("채팅방에 유저가 들어왔습니다")
                return json.dumps({}), 200
            elif event == "leave":
                print("채팅방에서 유저가 나갔습니다")
                return json.dumps({}), 200
            elif event == "send":
                user_text = body['textContent']['text']
                ret = get_answer_from_engine(bottype=bot_type, query=user_text)
                return naverEvent.send_resp(user_key, ret)

        else:
            abort(404)

    except Exception as ex:
        print(ex)
        abort(500)  # 오류 발생 시 500 오류


app.run()