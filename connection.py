import socket
from typing import Callable, Any, Literal
from threading import Thread

HEADER = 8
FORMAT = 'utf-8'


class Connection:
    
    '''A class that represents a connection. This will abstract away the complexities of network communication.'''
    
    @staticmethod
    def create_socket() -> socket.socket:
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    @staticmethod
    def get_local_ip_address_of_this_machine() -> str:
        return socket.gethostbyname(socket.gethostname())
    
    
    def __init__(self, connection: socket.socket) -> None:
        self.__connection = connection
        
    @property
    def connection(self) -> socket.socket:
        return self.__connection


    
    def send_bytes(self, data: bytes) -> None:
        self.__connection.send(data)

    def send_int(self, data: int, length: int, byteorder: Literal['little', 'big'] = 'little', signed: bool = False) -> None:
        self.send_bytes(
            data.to_bytes(
                length=length,
                byteorder=byteorder,
                signed=signed
            )
        )

    def send_bool(self, data: bool):
        self.send_int(int(data), 1)

    def send_string(self, data: str) -> None:


        message = data.encode(FORMAT)

        #sends length of message then sends the messages itself
        self.send_int(
            data=len(message),
            length=HEADER
        )

        self.send_bytes(message)
    
    def receive_bytes(self, length: int) -> bytes:
        data = self.__connection.recv(length)
        while not data:
            self.__connection.recv(length)
        return data
    
    def receive_int(self, length: int, byteorder: Literal['little', 'big'] = 'little', signed: bool = False) -> int:
        return int.from_bytes(self.receive_bytes(length), byteorder=byteorder, signed=signed)
    
    def receive_bool(self) -> bool:
        return bool(self.receive_int(1))
    
    def receive_string(self) -> str:
        length = self.receive_int(HEADER)
        message = self.receive_bytes(length)
        return message.decode(FORMAT)
    



class Client(Connection):
    
    def __init__(self, connection: socket.socket):
        super().__init__(connection)

    def connect(self, address: str, port: int) -> None:
        self.connection.connect((address, port))


    def disconnect(self) -> None:
        self.connection.close()



class Server(Connection):
    
    def __init__(self, connection: socket.socket):
        super().__init__(connection)
        self.__server_active = False


    @property
    def server_active(self) -> bool:
        return self.__server_active
    
    def bind(self,
                    address: str,
                    port: int,
                    handle_client_function: Callable[[socket.socket, str], Any]) -> None:
    
        self.connection.bind((address,port))
        self.connection.listen()

        self.__server_active = True

        while True:
            client_connection, client_ip_address = self.connection.accept()
            thread = Thread(
                target=handle_client_function,
                args=(client_connection, client_ip_address)
            )
            thread.start()

