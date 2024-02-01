from connection import Client


def main():
    client = Client(Client.create_socket())
    client.connect(Client.get_local_ip_address_of_this_machine(), 5050)
    print (client.send_bool(True))
    client.disconnect()


if __name__ == '__main__':
    main()