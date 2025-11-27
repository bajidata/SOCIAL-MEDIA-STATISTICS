# tgbot.py
import asyncio
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

from config.loader import TOKEN


async def start(update, context: ContextTypes.DEFAULT_TYPE):

    # Current datetime
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Send the first message
    await update.message.reply_text(f"🤖 Bot is already running — {now}")

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text="Open Social Media Dashboard",
                web_app=WebAppInfo(url="https://postordination-karleen-disinterested.ngrok-free.dev")
            )
        ]
    ])

    await update.message.reply_text(
        f"Click the button below to open the Social Media Statistic Dashboard",
        reply_markup=keyboard
    )


async def run_telegram_bot():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))

    print("🚀 Telegram bot started (non-blocking)!")

    # ---- IMPORTANT ----
    # 1) Initialize bot
    await application.initialize()

    # 2) Start application (but do NOT close the loop!)
    await application.start()

    # 3) Start polling manually (non-blocking)
    await application.updater.start_polling()

    # Keep bot alive
    # This prevents method from exiting
    await asyncio.Event().wait()
