import logging
import os
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# --- SOZLAMALAR ---
API_TOKEN = '8158239113:AAEg9b2m5Lx0GYs6WaKGwU1sdSn5I3TStwg' 
CHANNELS = ["@DJ_Baxtiyor"] 
YOUTUBE_URL = "https://youtube.com/@dj_baxtiyor_remix?si=wUWy2aIqTlDQcG0-" 
WEBSITE_URL = "https://leofame.com/free-instagram-views" 

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Koyeb uchun majburiy qism (Portni eshitish uchun)
async def handle(request):
    return web.Response(text="Bot is online!")

async def check_sub(user_id):
    for channel in CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status == 'left': return False
        except: return False
    return True

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if await check_sub(message.from_user.id):
        btn = InlineKeyboardMarkup().add(InlineKeyboardButton("🌐 Saytni ochish", web_app=WebAppInfo(url=WEBSITE_URL)))
        await message.answer("Xush kelibsiz!", reply_markup=btn)
    else:
        btn = InlineKeyboardMarkup(row_width=1)
        btn.add(InlineKeyboardButton("🔹 Kanalga a'zo bo'lish", url=f"https://t.me/{CHANNELS[0][1:]}"),
                InlineKeyboardButton("🎬 YouTube obuna", url=YOUTUBE_URL),
                InlineKeyboardButton("✅ Tekshirish", callback_data="check"))
        await message.answer("Avval kanallarga a'zo bo'ling:", reply_markup=btn)

@dp.callback_query_handler(text="check")
async def check_callback(call: types.CallbackQuery):
    if await check_sub(call.from_user.id):
        await call.message.delete()
        btn = InlineKeyboardMarkup().add(InlineKeyboardButton("🌐 Saytni ochish", web_app=WebAppInfo(url=WEBSITE_URL)))
        await call.message.answer("Rahmat! Saytga kiring:", reply_markup=btn)
    else:
        await call.answer("❌ Obuna bo'lmadingiz!", show_alert=True)

if __name__ == '__main__':
    # Koyeb veb-serveri
    app = web.Application()
    app.router.add_get('/', handle)
    port = int(os.environ.get("PORT", 8000)) # Rasmingizdagi portga mosladim
    
    loop = asyncio.get_event_loop()
    loop.create_task(web._run_app(app, host='0.0.0.0', port=port))
    
    # Botni yuritish
    executor.start_polling(dp, skip_updates=True)
