import socket, sys
# connect to www.google.com and request a page
# output whatever was sent to it onto the terminal
# Question 1: How to you specify a TCP socket in Python?

# create a TCP socket
def create_tcp_socket():
    print("Creating socket")
    try:
        # \/ Question 1 (SOCK_STREAM means TCP socket?)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except (socket.error, msg):
        print(f'Failed to create socket. Error: {str(msg[0])}, {msg[1]}')
        sys.exit()
    print("Socket created successfully")
    return s


# get host info
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname(host)
    except socket.gaierror as e:
        print("Hostname could not be resolved.", e)
        sys.exit()
    print(f'IP address of {host} is {remote_ip}')
    return remote_ip


# send data to a server
def send_data(serversocket, payload):
    print("Sending payload")
    try:
        # Don't want to encode it twice.
        if isinstance(payload, str):
            serversocket.sendall(payload.encode())
        else: # payload is already bytes; just send it
            serversocket.sendall(payload)
    except socket.error:
        print("Send failed")
        sys.exit()
    print("Payload send successfully")


def main():
    try:
        # define address info, payload, and buffer size
        host = 'www.google.com'
        port = 80
        payload = f'GET / HTTP/1.0\r\nHost: {host}\r\n\r\n'
        buffer_size = 4096

        # make the socket, get the IP, and connect
        s = create_tcp_socket()

        remote_ip = get_remote_ip(host)

        s.connect((remote_ip, port))
        print(f'Socket connected to {host} on IP {remote_ip}')

        # send the data and shutdown
        send_data(s, payload)
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
        print(full_data)
    except Exception as e:
        print(e)
    finally:
        # always close at the end!
        s.close()


if __name__ == "__main__":
    main()

