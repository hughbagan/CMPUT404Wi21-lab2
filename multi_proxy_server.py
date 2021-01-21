import socket, time
import multiprocessing as mp
import proxy_server

HOST = ""
PORT = 8001
BUFFER_SIZE = 4096


# Useful testing function 
# https://docs.python.org/3.6/library/multiprocessing.html#the-process-class
def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())


def handle_fork_connection(conn, addr):
    print("connected by", addr)
    full_data = conn.recv(BUFFER_SIZE)
    print("Received from client:", full_data)
    time.sleep(10)
    proxy_data = proxy_server.connect_to_google(full_data)
    print(proxy_data[:100], "...")
    conn.sendall(proxy_data)
    print("Sent to client.")
    conn.close()


def main():
    mp.set_start_method('fork') # (the default on Unix)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(2)
        while True: # continuously listen for connections
            conn, addr = s.accept()
            # Create a new Process for each new connection
            p = mp.Process(target=handle_fork_connection, args=(conn,addr))
            p.start()
            p.join()


if __name__=='__main__':
    main()