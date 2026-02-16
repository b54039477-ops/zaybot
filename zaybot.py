import asyncio
import logging
import os
from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.exceptions import TelegramBadRequest

# --- SOZLAMALAR ---
API_TOKEN = '8158239113:AAEg9b2m5Lx0GYs6WaKGwU1sdSn5I3TStwg'
CHANNELS = ["@DJ_Baxtiyor"]
YOUTUBE_URL = "https://youtube.com/@dj_baxtiyor_remix?si=wUWy2aIqTlDQcG0-"
WEBSITE_URL = "https://leofame.com/free-instagram-views"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Render/Koyeb uchun veb-server (Bot o'chib qolmasligi uchun)
async def handle(request):
    return web.Response(text="Bot is online!")

async def check_sub(user_id):
    for channel in CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status in ['left', 'kicked']:
                return False
        except Exception:
            return False
    return True

@dp.message(Command("start"))
async def start(message: types.Message):
    is_sub = await check_sub(message.from_user.id)
    if is_sub:
        btn = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🌐 Nakrutka urish", web_app=WebAppInfo(url=WEBSITE_URL))]
        ])
        await message.answer("Assalomu alaykum. Xush kelibsiz!", reply_markup=btn)
    else:
        btn = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔹 Kanalga a'zo bo'lish", url=f"https://t.me/{CHANNELS[0][1:]}")],
            [InlineKeyboardButton(text="🎬 YouTube obuna", url=YOUTUBE_URL)],
            [InlineKeyboardButton(text="✅ Tekshirish 🫆", callback_data="check")]
        ])
        await message.answer("Avval kanallarga a'zo bo'ling:", reply_markup=btn)

@dp.callback_query(F.data == "check")
async def check_callback(call: types.CallbackQuery):
    is_sub = await check_sub(call.from_user.id)
    if is_sub:
        await call.message.delete()
        btn = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🌐 Nakrutka urish", web_app=WebAppInfo(url=WEBSITE_URL))]
        ])
        await call.message.answer("Rahmat! Mendan bemalol foydalanishingiz mumkin! 👀:", reply_markup=btn)
    else:
        await call.answer("❌ Obuna bo'lmadingiz!", show_alert=True)

async def main():
    # Veb-serverni ishga tushirish
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.environ.get("PORT", 8080)))
    asyncio.create_task(site.start())

    # Botni ishga tushirish
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped!")
