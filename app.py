from flask import Flask, request

app = Flask(__name__)

@app.route('/get_ip', methods=['GET'])
def get_ip():
    # 获取请求者的公网IP地址
    user_ip = request.remote_addr
    return {"ip": user_ip}

if __name__ == '__main__':
    # 启动服务器，监听5010端口
    app.run(host='0.0.0.0', port=5010)
