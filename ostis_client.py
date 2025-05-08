from sc_client.client import connect, disconnect, is_connected

# Подключение к OSTIS серверу
url = "ws://localhost:8090/ws_json"

def connect_to_ostis():
    """ Функция для подключения к OSTIS серверу """
    connect(url)

    if is_connected():
        print("Успешное подключение к OSTIS серверу!")
    else:
        print("Нет подключения")
        disconnect()

