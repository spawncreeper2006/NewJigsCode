from typing import Literal


class User:
    '''A class that represents a user.'''

    def __init__(self,
                 user_id: int | None = None,
                 username: str | None = None,
                 password: str | None = None,
                 user_type: str | None = None,
                 position: str | None = None):


        self.__user_id = user_id
        self.__username = username
        self.__password = password
        self.__user_type = user_type
        self.__position = position



    @property
    def user_id(self) -> int:
        '''a unique numerical representation of the user'''
        if self.__user_id is None:
            raise AttributeError('cannot access this attribute as this object is not valid')

        return self.__user_id

    @property
    def username(self) -> str:
        '''a unique textual reference to a user that they choose'''
        if self.__username is None:
            raise AttributeError('cannot access this attribute as this object is not valid')

        return self.__username
    @property
    def password(self) -> str:
        '''a string representing of the users password'''
        if self.__password is None:
            raise AttributeError('cannot access this attribute as this object is not valid')

        return self.__password

    @property
    def user_type(self) -> Literal['Admin', 'User']:
        '''a string representing the type of the user'''
        if self.__user_type is None or (self.__user_type != 'Admin' and self.__user_type != 'User'):
            raise AttributeError('cannot access this attribute as this object is not valid')

        return self.__user_type

    @property
    def position(self) -> str:
        '''a string representing the position of the user in the company'''
        if self.__position is None:
            raise AttributeError('cannot access this attribute as this object is not valid')

        return self.__position


    @property
    def is_valid(self) -> bool:
        '''Returns a boolean based on if the instance represents an actual user or is null'''
        return self.__user_id is not None

    def __str__(self) -> str:
        if self.is_valid:
            return f'{self.username}, user_id={self.user_id}, password={self.password}, user_type={self.user_type}, position={self.position}'
        else:
            return 'placeholder user object'


if __name__ == '__main__':
    user = User(5,
                'me',
                'x',
                'Admin',
                'car')

