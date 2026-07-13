import asyncio, socket, os, logging, json
from telethon import TelegramClient, events

API_ID = 0  # <-- CAMBIAR: sacar de https://my.telegram.org
API_HASH = ""  # <-- CAMBIAR
BOT_TOKEN = "8774485792:AAF9G8BIi47uXvuhtXxILUluGzQdd3-Cl8E"
CHAT_ID = 7699121205
MAC = "10:FF:E0:65:C8:4C"
SESSION_FILE = "relay_session"
logging.basicConfig(level=logging.INFO)

def send_wol():
    mac_clean = MAC.replace("-", "").replace(":", "")
    mac_bytes = bytes.fromhex(mac_clean)
    magic = b"\xff" * 6 + mac_bytes * 16
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(magic, ("255.255.255.255", 9))
    sock.sendto(magic, ("192.168.1.255", 9))
    sock.close()
    logging.info("WOL broadcast enviado")

async def main():
    client = TelegramClient(SESSION_FILE, API_ID, API_HASH)
    await client.start()
    me = await client.get_me()
    logging.info(f"Conectado como {me.username or me.first_name}")

    @client.on(events.NewMessage(chats=CHAT_ID))
    async def handler(event):
        msg = event.message.text or ""
        if msg.strip() == "/wake" or msg.strip() == "🚀 WAKE":
            send_wol()

    logging.info("Esperando mensajes...")
    await client.run_until_disconnected()

asyncio.run(main())
