import os
import asyncio
import sys
import socket
import time
import json
import logging

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
from wakeonlan import wake
from ping3 import ping
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "8774485792:AAF9G8BIi47uXvuhtXxILUluGzQdd3-Cl8E"
MAC_ADDRESS = "10-FF-E0-65-C8-4C"
CHAT_ID = 7699121205
LOCAL_IP = "192.168.1.37"
PUBLIC_IP = "88.20.72.39"
WOL_PORT = 9
PUBLIC_WOL_PORT = 43001
STATUS_TCP_PORT = 43002
HEARTBEAT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "last_online.txt")
HEARTBEAT_LIMIT = 300

logging.basicConfig(level=logging.INFO)

def save_heartbeat():
    try:
        with open(HEARTBEAT_FILE, "w") as f:
            f.write(str(time.time()))
    except:
        pass

def load_heartbeat():
    try:
        with open(HEARTBEAT_FILE, "r") as f:
            return float(f.read().strip())
    except:
        return 0

def get_wol_target():
    if os.environ.get("CLOUD_MODE"):
        return PUBLIC_IP, PUBLIC_WOL_PORT
    return "255.255.255.255", WOL_PORT

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != CHAT_ID:
        await update.message.reply_text("No autorizado")
        return
    mode = " NUBE" if os.environ.get("CLOUD_MODE") else " LOCAL"
    await update.message.reply_text(
        f"Bot WOL activo [{mode}]\n"
        "/wake - Encender el PC\n"
        "/status - Ver si el PC esta encendido"
    )

async def wake(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != CHAT_ID:
        await update.message.reply_text("No autorizado")
        return
    try:
        target, port = get_wol_target()
        wake(MAC_ADDRESS, host=target, port=port)
        await update.message.reply_text(f"Paquete enviado a {target}:{port}")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def online(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != CHAT_ID:
        await update.message.reply_text("No autorizado")
        return
    save_heartbeat()
    await update.message.reply_text("OK")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != CHAT_ID:
        await update.message.reply_text("No autorizado")
        return
    try:
        if os.environ.get("CLOUD_MODE"):
            last = load_heartbeat()
            if time.time() - last < HEARTBEAT_LIMIT:
                await update.message.reply_text("PC ENCENDIDO")
            else:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                try:
                    r = sock.connect_ex((PUBLIC_IP, STATUS_TCP_PORT))
                    if r == 0:
                        await update.message.reply_text("PC ENCENDIDO (TCP)")
                    else:
                        r2 = ping(PUBLIC_IP, timeout=5)
                        if r2:
                            await update.message.reply_text("PC ENCENDIDO (ping)")
                        else:
                            await update.message.reply_text("PC APAGADO?")
                finally:
                    sock.close()
        else:
            r = ping(LOCAL_IP, timeout=5)
            if r:
                await update.message.reply_text(f"PC ENCENDIDO ({r*1000:.0f}ms)")
            else:
                await update.message.reply_text("PC APAGADO")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != CHAT_ID:
        await update.message.reply_text("No autorizado")
        return
    m = "NUBE" if os.environ.get("CLOUD_MODE") else "LOCAL"
    await update.message.reply_text(f"Modo: {m}")

def main():
    app = Application.builder().token(BOT_TOKEN).concurrent_updates(False).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("wake", wake))
    app.add_handler(CommandHandler("online", online))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("mode", mode))
    logging.info("Bot iniciado")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
