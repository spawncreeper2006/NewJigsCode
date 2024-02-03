import sqlite3

from abc import ABC, abstractmethod
from users import User
from typing import Any



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

    @property
    @abstractmethod
    def connection(self) -> sqlite3.Connection:
        '''holds an sqlite3 connection'''

    @property
    @abstractmethod
    def cursor(self) -> sqlite3.Cursor:
        '''holds an sqlite3 cursor'''

class Table(ABC):
    '''an abstract base class for tables to inherit from'''

    def query(self, field_name: str, field_value: Any) -> Any:
        '''queries the database'''

        self.database.cursor.execute(
            f"SELECT * FROM {self.table_name} WHERE {field_name}=?",
            (field_value,)
            )

        results = self.database.cursor.fetchall()
        return results

    @abstractmethod
    def insert_into(self, insert_data: Any) -> None:
        '''inserts a record into the table'''

    @property
    @abstractmethod
    def database(self) -> Database:
        '''an instance of the database class for low level SQL operations'''

    @property
    @abstractmethod
    def table_name(self) -> str:
        '''holds the name of the table'''




class UsersDatabase(Database):
    '''A class that interfaces with the user database'''
    def __init__(self, filename: str) -> None:
        self.filename: str = filename
        self.__connection: sqlite3.Connection | None = None
        self.__cursor: sqlite3.Cursor | None = None

    @property
    def connected(self) -> bool:
        return self.__connection is not None and self.__cursor is not None

    @property
    def connection(self) -> sqlite3.Connection:
        if self.__connection is None:
            raise ConnectionError('trying to access connection property with no active connection')
        return self.__connection

    @property
    def cursor(self) -> sqlite3.Cursor:
        if self.__cursor is None:
            raise ConnectionError('trying to accesss cursor property with no active connection')
        return self.__cursor

    def connect(self) -> None:
        self.__connection = sqlite3.connect(self.filename)
        self.__cursor = self.connection.cursor()

    def disconnect(self) -> None:

        self.connection.close()

        self.__connection = None
        self.__cursor = None

class UsersTable(Table):
    '''a class that interfaces with the user table'''
    def __init__(self, database: UsersDatabase) -> None:
        self.__database = database

    @property
    def database(self) -> UsersDatabase:
        return self.__database

    @property
    def table_name(self) -> str:
        return 'users'

    def query(self, field_name: str, field_value: Any) -> User:
        results = super().query(field_name, field_value)

        if len(results) != 1:
            return User()

        result = results[0]

        if len(result) != 5:
            return User()

        return User(*result)

    def insert_into(self, insert_data: User) -> None:

        self.database.cursor.execute(
            '''INSERT INTO users(UserID, Username, Password, UserType, Position)
            VALUES(?,?,?,?,?) ''',
            (insert_data.user_id, insert_data.username, insert_data.password, insert_data.user_type, insert_data.position)
        )

        self.database.connection.commit()


class FriendsTable(Table):
    '''a class that interfaces with the contacts table'''
    def __init__(self, database: UsersDatabase) -> None:
        self.__database = database

    @property
    def database(self) -> UsersDatabase:
        return self.__database

    @property
    def table_name(self) -> str:
        return 'friends'


    def query(self, field_name: str, field_value: Any) -> Any:

        self.database.cursor.execute(f'SELECT * FROM friends WHERE {field_name}=?', (field_value,))
        return self.database.cursor.fetchall()

    @staticmethod
    def __add_friend_to_list(friends: list[User], friend_id: int, users_table: UsersTable) -> None:
        friends.append(
            users_table.query(
                'UserID',
                friend_id
            )
        )


    def find_friends(self, user_id: int, users_table: UsersTable) -> list[User]:
        '''returns a list of friends'''
        friends: list[User] = []

        # reponse is a tuple with the known user id followed by the friend user id
        for response in self.query('UserID', user_id):
            FriendsTable.__add_friend_to_list(friends, response[1], users_table)



        for response in self.query('FriendID', user_id):
            FriendsTable.__add_friend_to_list(friends, response[0], users_table)


        return friends

    def insert_into(self, insert_data: tuple[User, User]) -> None:


        self.database.cursor.execute(
            '''INSERT INTO friends(UserID, FriendID)
            VALUES(?,?) ''',
            (insert_data[0].user_id, insert_data[1].user_id)
        )

        self.database.connection.commit()


class MessageLineTable(Table):
    '''a class that interfaces with the message line table'''

    def __init__(self, database: UsersDatabase) -> None:
        self.__database = database

    @property
    def database(self) -> UsersDatabase:
        return self.__database

    def query(self, field_name: str, field_value: str):
        pass



def main():
    '''testing main function'''
    db = UsersDatabase('users.db')
    db.connect()

    ct = FriendsTable(db)
    ut = UsersTable(db)


    user1 = ut.query('UserID', 1)
    user2 = ut.query('UserID', 7)

    ct.insert_into((
        user1,
        user2
    ))

    db.disconnect()




if __name__ == '__main__':
    main()
