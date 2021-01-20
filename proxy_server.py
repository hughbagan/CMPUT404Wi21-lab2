# This script is both a server and a client
import socket, sys, time
import client


def connectToGoogle(payload):
    # eg. payload = f'GET / HTTP/1.0\r\nHost: {host}\r\n\r\n'
    proxy_data = b"" # bytestring!
    try:
        # define address info, payload, and buffer size
        host = 'www.google.com'
        port = 80
        buffer_size = 4096
        # make the socket, get the IP, and connect
        s = client.create_tcp_socket()
        remote_ip = client.get_remote_ip(host)
        s.connect((remote_ip, port))
        print(f'Socket connected to {host} on IP {remote_ip}')
        # send the data and shutdown
        client.send_data(s, payload)
        s.shutdown(socket.SHUT_WR)
        # continue accepting data until no more is left
        while True:
            data = s.recv(buffer_size)
            if not data:
                print(data)
                break
            proxy_data += data
        print("Data from", host, "received")
        #print(proxy_data)
    except Exception as e:
        print(e)
    finally:
        s.close() # always close at the end!
    return proxy_data


def main():
    # Listen for connections from proxy_client.py (localhost)
    HOST = ""
    PORT = 8001
    BUFFER_SIZE = 4096
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT)) # bind socket to address
        s.listen(2) # set to listening mode
        while True: # continuously listen for connections
            conn, addr = s.accept()
            print("connected by", addr)
            # Should be a request
            full_data = conn.recv(BUFFER_SIZE)
            print("Received from client:", full_data)
            time.sleep(0.5)

            proxy_data = connectToGoogle(full_data)
            print(proxy_data[:200], "...")

            # send the res. from google back to proxy_client.py
            conn.sendall(proxy_data)
            print("Sent to client.")
            conn.close()


if __name__ == "__main__":
    main()
