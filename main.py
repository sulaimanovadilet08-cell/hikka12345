from flask import Flask
from threading import Thread
from telethon import TelegramClient, events
import asyncio

# 🌐 Flask-сервер для UptimeRobot
app = Flask('')

@app.route('/')
def home():
    return "I'm alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 🔧 Настройки Telegram API
api_id = 25704479
api_hash = "a6d27fc2500314ab597a057b8e8761b3"

client = TelegramClient('session', api_id, api_hash)

mining = False
OWNER_ID = None  # будет установлен после запуска

# ✅ Команды
@client.on(events.NewMessage(pattern='.ктолох'))
async def ping_handler(event):
    await event.reply('@waaysexz лох')
    
@client.on(events.NewMessage(pattern='/ping'))
async def ping_handler(event):
    await event.reply('Pong! Я жив!')

@client.on(events.NewMessage(pattern='/help'))
async def help_handler(event):
    await event.reply(
        "📋 Команды юзербота:\n"
        "/ping — проверить, жив ли бот\n"
        "/help — показать это сообщение\n"
        ".mine — начать спамить 'коп' в @mine_evo_gold_bot\n"
        ".stopmine — остановить спам\n"
       ".ктолох - проверка на лохов"
    )

@client.on(events.NewMessage(pattern=r'\.mine'))
async def start_mine(event):
    if event.sender_id != OWNER_ID:
        return
    global mining
    if mining:
        await event.reply("⛏ Уже майню...")
        return
    await event.reply("🚀 Начинаю майнить в @mine_evo_gold_bot")
    mining = True
    while mining:
        try:
            await client.send_message("@mine_evo_gold_bot", "коп")
            await asyncio.sleep(2.5)
        except Exception as e:
            await event.reply(f"❌ Ошибка при отправке: {e}")
            break

@client.on(events.NewMessage(pattern=r'\.stopmine'))
async def stop_mine(event):
    if event.sender_id != OWNER_ID:
        return
    global mining
    if mining:
        mining = False
        await event.reply("🛑 Майн остановлен.")
    else:
        await event.reply("⚠️ Сейчас не майню.")

# 🔁 Периодический вывод в консоль
async def keep_alive_ping():
    while True:
        print("✅ Бот активен...")
        await asyncio.sleep(60)

# 🔧 Основной запуск
async def main():
    global OWNER_ID
    await client.start()
    me = await client.get_me()
    OWNER_ID = me.id
    print(f"🔋 Юзербот запущен как @{me.username} (ID: {OWNER_ID})")
    await asyncio.gather(client.run_until_disconnected(), keep_alive_ping())

# 🟢 Запуск
keep_alive()  # <-- ДОЛЖНО БЫТЬ ДО with client
with client:
    client.loop.run_until_complete(main())
