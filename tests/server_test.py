from connection import Server, Client, Connection
from socket import socket


def handle_client_function(_socket: socket, ip_addr: str):
    print ('new client connected')
    conn = Client(_socket)
    print (conn.receive_bool())
    conn.disconnect()
    

def main():

    conn = Server(Connection.create_socket())
    conn.bind(Connection.get_local_ip_address_of_this_machine(),
                        5050,
                        handle_client_function,
                        )


if __name__ == '__main__':
    main()