import os, asyncio, sys, socket, time, json, logging
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
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
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HEARTBEAT_FILE = os.path.join(BASE_DIR, "last_online.txt")
STATE_FILE = os.path.join(BASE_DIR, "pc_state.txt")

logging.basicConfig(level=logging.INFO)

def send_wol(mac, host, port):
    mac_clean = mac.replace("-", "").replace(":", "").replace(".", "")
    mac_bytes = bytes.fromhex(mac_clean)
    magic = b"\xff" * 6 + mac_bytes * 16
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(magic, (host, port))
    sock.close()

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
        return 0.0

def save_state(state):
    try:
        with open(STATE_FILE, "w") as f:
            f.write(f"{state}:{time.time()}")
    except:
        pass

def load_state():
    try:
        with open(STATE_FILE, "r") as f:
            parts = f.read().strip().split(":", 1)
            return parts[0], float(parts[1])
    except:
        return "OFF", 0.0

def get_wol_target():
    if os.environ.get("CLOUD_MODE"):
        return PUBLIC_IP, PUBLIC_WOL_PORT
    return "255.255.255.255", WOL_PORT

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != CHAT_ID:
        return
    m = "NUBE" if os.environ.get("CLOUD_MODE") else "LOCAL"
    await update.message.reply_text(
        f"Bot WOL [{m}]\n"
        "/wake - Encender PC\n"
        "/status - Estado del PC"
    )

async def wake(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != CHAT_ID:
        return
    try:
        target, port = get_wol_target()
        send_wol(MAC_ADDRESS, target, port)
        save_heartbeat()
        save_state("ON")
        await context.bot.send_message(chat_id=CHAT_ID, text="\U0001f680 WAKE")
        await update.message.reply_text(f"Paquete enviado a {target}:{port}")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != CHAT_ID:
        return
    try:
        if not os.environ.get("CLOUD_MODE"):
            r = ping(LOCAL_IP, timeout=5)
            await update.message.reply_text(f"PC ENCENDIDO ({r*1000:.0f}ms)" if r else "PC APAGADO")
            return

        last_hb = load_heartbeat()
        state, state_time = load_state()
        now = time.time()
        hb_age = now - last_hb

        if hb_age < 120:
            await update.message.reply_text("PC ENCENDIDO")
            return

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        try:
            if sock.connect_ex((PUBLIC_IP, STATUS_TCP_PORT)) == 0:
                await update.message.reply_text("PC ENCENDIDO")
                return
        finally:
            sock.close()

        if state == "OFF":
            await update.message.reply_text("PC APAGADO")
        elif state == "SLEEP" or hb_age < 600:
            await update.message.reply_text("PC EN SUSPENSION")
        else:
            await update.message.reply_text("PC APAGADO")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def online(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != CHAT_ID:
        return
    save_heartbeat()
    save_state("ON")
    await update.message.reply_text("OK")

async def sleep_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != CHAT_ID:
        return
    save_state("SLEEP")
    await update.message.reply_text("OK")

async def offline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != CHAT_ID:
        return
    save_state("OFF")
    await update.message.reply_text("OK")

async def mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != CHAT_ID:
        return
    m = "NUBE" if os.environ.get("CLOUD_MODE") else "LOCAL"
    await update.message.reply_text(f"Modo: {m}")

def main():
    app = Application.builder().token(BOT_TOKEN).concurrent_updates(False).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("wake", wake))
    app.add_handler(CommandHandler("online", online))
    app.add_handler(CommandHandler("sleep", sleep_cmd))
    app.add_handler(CommandHandler("offline", offline))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("mode", mode))
    logging.info("Bot iniciado")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
