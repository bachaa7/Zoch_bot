import asyncio
from sc_client.client import connect, disconnect, is_connected

# Подключение к OSTIS серверу
url = "ws://localhost:8090/ws_json"
connect(url)

if is_connected():
    print("Успешное подключение к OSTIS серверу!")

else: 
    print("Нет подключения")
    
    
    
    
    






disconnect()
