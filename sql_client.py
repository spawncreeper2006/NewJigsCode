import sqlite3

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Literal

class Database(ABC):
    '''an abstract base class for databases to inherit from'''
    @abstractmethod
    def connect(self) -> None:
        '''connects to the database'''

    @abstractmethod
    def disconnect(self) -> None:
        '''disconnects from database'''

    @property
    @abstractmethod
    def connected(self) -> bool:
        '''holds a boolean based on if the database class is connected or not'''


class Table(ABC):
    '''an abstract base class for tables to inherit from'''
    @abstractmethod
    def query(self, field_name: str, field_value: Any) -> Any:
        '''queries the table for any record that has a field matching the field value'''

    @abstractmethod
    def insert_into(self, insert_data: Any) -> None:
        '''inserts a record into the table'''

    @property
    @abstractmethod
    def database(self) -> Database:
        '''an instance of the database class for low level SQL operations'''


@dataclass
class User:
    '''A dataclass that represents an account.'''
    user_id: int | None = None
    username: str | None = None
    password: str | None = None
    user_type: Literal['Admin', 'User'] | None = None
    position: str | None = None

    @property
    def is_valid(self) -> bool:
        '''Returns a boolean based on if the instance represents an actual user or is null'''
        return self.user_id is not None



class UsersDatabase(Database):
    '''A class that interfaces with the user database'''
    def __init__(self, filename: str) -> None:
        self.filename: str = filename
        self.connection: sqlite3.Connection | None = None
        self.cursor: sqlite3.Cursor | None = None

    @property
    def connected(self) -> bool:
        return self.connection is not None and self.cursor is not None

    def connect(self) -> None:
        self.connection = sqlite3.connect(self.filename)
        self.cursor = self.connection.cursor()

    def disconnect(self) -> None:
        if isinstance(self.connection, sqlite3.Connection):
            self.connection.close()


        else:
            print ('disconnect was called on closed connection')

        self.connection = None
        self.cursor = None

class UsersTable(Table):
    '''a class that interfaces with the user table'''
    def __init__(self, database: UsersDatabase) -> None:
        self.__database = database

    @property
    def database(self) -> UsersDatabase:
        return self.__database

    def query(self, field_name: str, field_value: str) -> User:

        if self.database.connection is None or self.database.cursor is None:
            raise ConnectionError('Cannot query database with no active connection')


        self.database.cursor.execute(f"SELECT * FROM users WHERE {field_name}=?", (field_value,))

        results = self.database.cursor.fetchall()

        if len(results) != 1:
            return User()

        result = results[0]

        if len(result) != 5:
            return User()

        return User(*result)

    def insert_into(self, insert_data: User) -> None:
        if self.database.connection is None or self.database.cursor is None:
            raise ConnectionError('Cannot insert into database with no active connection')

        self.database.cursor.execute(
            '''INSERT INTO users(UserID, Username, Password, UserType, Position)
            VALUES(?,?,?,?,?) ''',
            (insert_data.user_id, insert_data.username, insert_data.password, insert_data.user_type, insert_data.position)
        )

        self.database.connection.commit()

class ContactsTable(Table):
    '''a class that interfaces with the contacts table'''
    def __init__(self, database: UsersDatabase) -> None:
        self.__database = database

    @property
    def database(self) -> UsersDatabase:
        return self.__database


    def query(self, field_name: str, field_value: Any) -> Any:

        if self.database.connection is None or self.database.cursor is None:
            raise ConnectionError('Cannot query database with no active connection')

        self.database.cursor.execute(f'SELECT * FROM friends WHERE {field_name}=?', (field_value,))
        return self.database.cursor.fetchall()


    def find_friends(self, user_id: int, users_table: UsersTable) -> list[User]:
        '''returns a list of friends'''
        friends: list[User] = []
        for response in self.query('UserID', user_id):
            # reponse is a tuple with the known user id followed by the friend user id
            friends.append(
                users_table.query(
                    'UserID',
                    response[1]
                )
            )

        return friends

    def insert_into(self, insert_data: Any) -> None:
        raise NotImplementedError('implement me')


def main():
    '''testing main function'''
    db = UsersDatabase('users.db')
    db.connect()
    ct = ContactsTable(db)
    ut = UsersTable(db)

    print (ct.find_friends(
        1,
        ut
    ))





if __name__ == '__main__':
    main()
