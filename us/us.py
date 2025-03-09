from flask import Flask, request, jsonify
import socket
import requests

app = Flask(__name__)

@app.route('/fibonacci', methods=['GET'])
def handle_request():
    # 获取请求参数
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')
    
    # 验证所有参数是否存在
    if not all([hostname, fs_port, number, as_ip, as_port]):
        return "400 Bad Request: Missing parameters", 400
    
    try:
        # 创建DNS查询
        dns_query = f"TYPE=A\nNAME={hostname}"
        
        # 发送UDP查询请求
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(dns_query.encode('utf-8'), (as_ip, int(as_port)))
        
        # 等待响应
        sock.settimeout(5.0)
        response, _ = sock.recvfrom(1024)
        sock.close()
        
        # 解析DNS响应
        lines = response.decode('utf-8').strip().split('\n')
        fs_ip = None
        
        for line in lines:
            if line.startswith('VALUE='):
                fs_ip = line.split('=')[1]
                break
        
        if not fs_ip:
            return "404 Not Found: Fibonacci server not found", 404
        
        # 发送请求到Fibonacci服务器
        fs_url = f"http://{fs_ip}:{fs_port}/fibonacci?number={number}"
        fs_response = requests.get(fs_url, timeout=5.0)
        
        # 返回结果
        return fs_response.text, fs_response.status_code
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)