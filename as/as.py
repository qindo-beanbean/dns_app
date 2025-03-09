import socket
import json
import os

# 端口配置
UDP_PORT = 53533

# 存储DNS记录的文件
DNS_FILE = "dns_records.json"

# 确保DNS记录文件存在
if not os.path.exists(DNS_FILE):
    with open(DNS_FILE, "w") as f:
        json.dump({}, f)

def load_dns_records():
    with open(DNS_FILE, "r") as f:
        return json.load(f)

def save_dns_records(records):
    with open(DNS_FILE, "w") as f:
        json.dump(records, f)

def handle_registration(data):
    # 解析注册请求
    lines = data.strip().split('\n')
    record = {}
    
    for line in lines:
        if line.startswith('TYPE='):
            record['type'] = line.split('=')[1]
        elif line.startswith('NAME='):
            record['name'] = line.split('=')[1]
        elif line.startswith('VALUE='):
            record['value'] = line.split('=')[1]
        elif line.startswith('TTL='):
            record['ttl'] = line.split('=')[1]
    
    # 存储记录
    if 'name' in record and 'value' in record:
        dns_records = load_dns_records()
        dns_records[record['name']] = record
        save_dns_records(dns_records)
        return True
    return False

def handle_query(data):
    # 解析查询请求
    lines = data.strip().split('\n')
    query = {}
    
    for line in lines:
        if line.startswith('TYPE='):
            query['type'] = line.split('=')[1]
        elif line.startswith('NAME='):
            query['name'] = line.split('=')[1]
    
    # 查找记录
    if 'name' in query:
        dns_records = load_dns_records()
        if query['name'] in dns_records:
            record = dns_records[query['name']]
            response = f"TYPE={record['type']}\nNAME={record['name']}\nVALUE={record['value']}\nTTL={record.get('ttl', '10')}"
            return response
    
    return None

def main():
    # 创建UDP套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', UDP_PORT))
    
    print(f"Authoritative Server running on UDP port {UDP_PORT}...")
    
    while True:
        data, addr = sock.recvfrom(1024)
        request = data.decode('utf-8')
        
        # 判断是注册请求还是查询请求
        if 'VALUE=' in request:
            # 处理注册请求
            success = handle_registration(request)
            if success:
                sock.sendto(b"Successfully registered", addr)
        else:
            # 处理查询请求
            response = handle_query(request)
            if response:
                sock.sendto(response.encode('utf-8'), addr)

if __name__ == "__main__":
    main()