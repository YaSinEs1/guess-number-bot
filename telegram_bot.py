import os
import random

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = os.getenv("TOKEN")

players = {}
records = {}

keyboard = ReplyKeyboardMarkup(
    [
        ["🎮 New Game"],
        ["🏆 My Record", "❓ Help"]
    ],
    resize_keyboard=True
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    players[user_id] = {
        "number": random.randint(1, 99),
        "tries": 0
    }

    await update.message.reply_text(
        "🎲 I picked a number between 1 and 99.\nTry to guess it!",
        reply_markup=keyboard
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎮 Number Guessing Game\n\n"
        "1. Start a game.\n"
        "2. Send a number.\n"
        "3. Bigger or Smaller.\n\nGood luck! 😄"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if text == "🎮 New Game":
        await start(update, context)
        return

    if text == "🏆 My Record":
        if user_id in records:
            await update.message.reply_text(
                f"🏆 Best record: {records[user_id]} attempts"
            )
        else:
            await update.message.reply_text("No record yet")
        return

    if text == "❓ Help":
        await help_command(update, context)
        return

    if user_id not in players:
        await update.message.reply_text("Start a game first")
        return

    try:
        guess = int(text)
    except:
        await update.message.reply_text("Send a number")
        return

    players[user_id]["tries"] += 1

    answer = players[user_id]["number"]
    tries = players[user_id]["tries"]

    if guess < answer:
        await update.message.reply_text(f"⬆️ Bigger! ({tries})")

    elif guess > answer:
        await update.message.reply_text(f"⬇️ Smaller! ({tries})")

    else:
        if user_id not in records or tries < records[user_id]:
            records[user_id] = tries

        await update.message.reply_text(
            f"🎉 Correct in {tries} tries!\n🏆 Best: {records[user_id]}"
        )

        del players[user_id]


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot is running...")
app.run_polling()
