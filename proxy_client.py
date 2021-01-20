# Send to proxy_server.py on localhost, print what's returned
import socket, sys
import client

def main():
    try:
        # Should match what proxy_server.py is expecting
        host = ""
        port = 8001
        # Should go thru the proxy to google and back
        payload = f'GET / HTTP/1.0\r\nHost: {host}\r\n\r\n'
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
        full_data = b"" # bytestring!
        while True:
            # "receive" and specify buffer size (amount of data to get)
            data = s.recv(buffer_size)
            if not data:
                print(data)
                break
            full_data += data
        print(full_data[:200], "...")
    except Exception as e:
        print(e)
    finally:
        # always close at the end!
        s.close()


if __name__ == "__main__":
    main()

