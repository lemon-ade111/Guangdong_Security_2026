import socket


def main():
    host = "www.baidu.com"
    port = 80

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((host, port))

        # 发送请求头（留空，按你的实验需求填写）
        request_header = "GET / HTTP/1.1\r\nHost: www.baidu.com\r\nConnection: close\r\n\r\n"
        # client.sendall(b"")
        client.sendall(request_header.encode('utf-8'))

        response = client.recv(1024)
        print(f"--- 捕获到服务器响应 --- \n{response.decode('utf-8', errors='ignore')[:500]}")


if __name__ == "__main__":
    main()
