import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from fastapi import FastAPI, Request
import uvicorn
import asyncio

TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", 8000))

app_bot = Application.builder().token(TOKEN).build()
web = FastAPI()

# -------- BOT --------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot ishlayapti ✅")

app_bot.add_handler(CommandHandler("start", start))

# -------- WEBHOOK --------
@web.post("/webhook")
async def telegram_webhook(req: Request):
    data = await req.json()
    update = Update.de_json(data, app_bot.bot)
    await app_bot.process_update(update)
    return {"ok": True}

@web.on_event("startup")
async def on_startup():
    await app_bot.bot.set_webhook(
        url=os.getenv("WEBHOOK_URL") + "/webhook"
    )

# -------- RUN --------
if __name__ == "__main__":
    uvicorn.run(web, host="0.0.0.0", port=PORT)
