import socket
from multiprocessing import Pool

HOST = "localhost"
PORT = 8081

def main():
    address = [('127.0.0.1', 8001)]
    # establish 10 different connections
    