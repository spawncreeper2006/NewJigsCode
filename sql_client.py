import sqlite3

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Literal

class SQLClient(ABC):

    @abstractmethod
    def connect(self) -> None:
        ...

    @abstractmethod
    def disconnect(self) -> None:
        ...

    @abstractmethod
    def query(self, field_name: str, field_value: Any) -> Any:
        ...

    @abstractmethod
    def insert_into(self, insert_data: Any) -> None:
        ...


@dataclass
class LoginQueryResponse:
    user_id: int | None = None
    username: str | None = None
    password: str | None = None
    user_type: Literal['Admin', 'User'] | None = None
    position: str | None = None

    @property
    def is_valid(self) -> bool:
        return self.user_id != None


class LoginClient(SQLClient):

    def __init__(self, filename: str) -> None:
        self.filename: str = filename
        self.connection: sqlite3.Connection | None = None
        self.cursor: sqlite3.Cursor | None = None

    @property
    def connected(self) -> bool:
        return self.connection != None

    def connect(self) -> None:
        self.connection = sqlite3.connect(self.filename)
        self.cursor = self.connection.cursor()

    def disconnect(self) -> None:
        if type(self.connection) == sqlite3.Connection:
            self.connection.close()
            
        else:
            print ('disconnect was called on closed connection')
        
        self.connection = None
        self.cursor = None

    def query(self, field_name: str, field_value: str) -> LoginQueryResponse:

        if self.cursor == None:
            raise Exception('Cannot query database with no active connection')
            
        
        self.cursor.execute(f"SELECT * FROM contacts WHERE {field_name}=?", (field_value,))

        results = self.cursor.fetchall()

        if len(results) != 1:
            return LoginQueryResponse()
        
        result = results[0]

        if len(result) != 5:
            return LoginQueryResponse()

        return LoginQueryResponse(*result)
    
    def insert_into(self, insert_data: LoginQueryResponse) -> None:
        
        if self.connection == None or self.cursor == None:
            raise Exception('Cannot insert into database with no active connection')
        

        
        self.cursor.execute(
            '''INSERT INTO contacts(UserID, Username, Password, UserType, Position)
            VALUES(?,?,?,?,?) ''',
            (insert_data.user_id, insert_data.username, insert_data.password, insert_data.user_type, insert_data.position)
        )

        self.connection.commit()

        





if __name__ == '__main__':
    lc = LoginClient('contact.db')
    lc.connect()
    
    lc.insert_into(LoginQueryResponse(
        5,
        'test1',
        'test1',
        'User',
        'Car'
    ))
    
    lc.disconnect()