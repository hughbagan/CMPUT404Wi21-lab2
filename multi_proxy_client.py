import socket, time
from multiprocessing import Pool

HOST = "www.google.com"
PORT = 8081
BUFFER_SIZE = 4096
payload = f'GET / HTTP/1.0\r\nHost: {HOST}\r\n\r\n'


def connect_to_server(address):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(address)
        s.sendall(payload.encode())
        s.shutdown(socket.SHUT_WR)
        full_data = s.recv(BUFFER_SIZE)
        print(full_data[:100])
    except Exception as e:
        print(e)
    finally:
        s.close()


def main():
    address = [('127.0.0.1', 8001)]
    # establish 10 different connections
    with Pool() as p:
        p.map(connect_to_server, address*10)
    # for i in range(10):
    #     p = Pool()
    #     p.map(connect_to_server, address)
        #time.sleep(1)


if __name__ == "__main__":
    main()

