
import tree_encryption



class EncryptionType:
    
    @staticmethod
    def encrypt(data: str) -> str:
        ...

    @staticmethod
    def decrypt(data: str) -> str:
        ...


class TreeEncrypt(EncryptionType):

    @staticmethod
    def __encrypt_or_decrypt(data: str) -> str:
        node = tree_encryption.construct_tree(data)
        node = tree_encryption.swap_nodes(node)
        if node != None:
            return tree_encryption.tree_to_string(node)
        else:
            raise Exception('the swap nodes function returned None')


    @staticmethod
    def encrypt(data: str) -> str:
        return TreeEncrypt.__encrypt_or_decrypt(data)

    @staticmethod   
    def decrypt(data: str) -> str:
        return TreeEncrypt.__encrypt_or_decrypt(data)

class AsciiEncrypt(EncryptionType):

    @staticmethod
    def __str_to_ascii_list(data: str) -> list[int]:
        return list(map(ord, data))
    
    @staticmethod
    def __ascii_list_to_str(data: list[int]) -> str:
        return ''.join(list(map(chr, data)))
    
    @staticmethod
    def __encrypt_or_decrypt(data: str, key: int, encrypt: bool) -> str:
        encrypt_number: int = 1 if encrypt else -1
        ascii_list = AsciiEncrypt.__str_to_ascii_list(data)
        ascii_list = [(ascii_value + key * encrypt_number) % 256 for ascii_value in ascii_list]
        return AsciiEncrypt.__ascii_list_to_str(ascii_list)
    
    @staticmethod
    def encrypt(data: str, key: int = 1) -> str:
        return AsciiEncrypt.__encrypt_or_decrypt(data, key, True)
    
    @staticmethod
    def decrypt(data: str, key: int = 1) -> str:
        return AsciiEncrypt.__encrypt_or_decrypt(data, key, False)
    


if __name__ == '__main__':
    print (TreeEncrypt.encrypt('hello world'))
