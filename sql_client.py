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
    def query(self, search_data: Any) -> Any:
        ...


@dataclass
class LoginQueryResponse:
    user_id: int | None = None
    username: str | None = None
    password: str | None = None
    user_type: Literal['Admin', 'User'] | None = None
    position: str | None = None


class LoginClient(SQLClient):

    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.connection = None
        self.cursor = None

    @property
    def connected(self) -> bool:
        return self.connection != None

    def connect(self) -> None:
        self.connection = sqlite3.connect(self.filename)
        self.cursor = self.connection.cursor()

    def disconnect(self) -> None:
        self.connection.close()
        self.connection = None
        self.cursor = None

    def query(self, username: str) -> LoginQueryResponse:
        if not self.connected:
            raise Exception('cannot query a database with no connection')
        
        self.cursor.execute("SELECT * FROM contacts WHERE username=?", (username,))

        results = self.cursor.fetchall()

        if len(results) != 1:
            return LoginQueryResponse()
        
        result = results[0]

        if len(result) != 5:
            return LoginQueryResponse()

        return LoginQueryResponse(*result)



if __name__ == '__main__':
    lc = LoginClient('contact.db')
    lc.connect()
    lqr = lc.query('yarr')

    print (lqr)