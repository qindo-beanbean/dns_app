from flask import Flask, request, jsonify
import socket
import requests
import json

app = Flask(__name__)

# Fibonacci计算函数
def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)

@app.route('/register', methods=['PUT'])
def register():
    try:
        # 解析请求体
        data = request.json
        hostname = data.get('hostname')
        ip = data.get('ip')
        as_ip = data.get('as_ip')
        as_port = int(data.get('as_port'))
        
        # 创建DNS注册消息
        dns_message = f"TYPE=A\nNAME={hostname}\nVALUE={ip}\nTTL=10"
        
        # 发送UDP注册请求
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(dns_message.encode('utf-8'), (as_ip, as_port))
        
        # 等待响应
        sock.settimeout(5.0)
        response, _ = sock.recvfrom(1024)
        sock.close()
        
        return "201 Created", 201
    except Exception as e:
        return str(e), 400

@app.route('/fibonacci', methods=['GET'])
def get_fibonacci():
    try:
        number = request.args.get('number')
        
        # 检查参数
        if not number or not number.isdigit():
            return "400 Bad Request", 400
            
        # 计算斐波那契数
        result = fibonacci(int(number))
        
        return jsonify({"fibonacci": result}), 200
    except Exception as e:
        return str(e), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)