import asyncio
import websockets
import json
import os

# Mesajları tutacak bir liste
messages = []

# Mesajları dosyaya kaydetme fonksiyonu
def save_messages():
    try:
        with open('messages.json', 'w') as f:
            json.dump(messages, f)
    except Exception as e:
        print(f"Error saving messages: {e}")

# Mesajları dosyadan yükleme fonksiyonu
def load_messages():
    global messages
    try:
        if os.path.exists('messages.json'):
            with open('messages.json', 'r') as f:
                messages = json.load(f)
        else:
            print("messages.json does not exist. A new one will be created.")
    except Exception as e:
        print(f"Error loading messages: {e}")

async def chat_handler(websocket, path):
    # WebSocket bağlantısı açıldığında önceki mesajları yükle
    load_messages()

    try:
        # Yeni bağlantı açıldığında, tüm mevcut mesajları gönder
        for message in messages:
            await websocket.send(json.dumps(message))

        while True:
            message = await websocket.recv()
            data = json.loads(message)

            # Mesajı listeye ekle
            messages.append(data)

            # Mesajları dosyaya kaydet
            save_messages()

            # Tüm kullanıcılara mesajı gönder
            await websocket.send(message)
    except websockets.exceptions.ConnectionClosed:
        print("Connection closed")

start_server = websockets.serve(chat_handler, 'localhost', 8765)

# Sunucu başlatma
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
