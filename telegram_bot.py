import os
import random
from flask import Flask, request

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("TOKEN")

app = Flask(__name__)

bot = Application.builder().token(TOKEN).build()

players = {}
records = {}

keyboard = ReplyKeyboardMarkup(
    [["🎮 New Game"], ["🏆 My Record", "❓ Help"]],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    players[user_id] = {"number": random.randint(1, 99), "tries": 0}

    await update.message.reply_text("🎲 Guess 1-99", reply_markup=keyboard)

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if text == "🎮 New Game":
        return await start(update, context)

    if user_id not in players:
        return await update.message.reply_text("Start game first")

    try:
        guess = int(text)
    except:
        return

    players[user_id]["tries"] += 1
    answer = players[user_id]["number"]

    if guess < answer:
        await update.message.reply_text("⬆️ Bigger")
    elif guess > answer:
        await update.message.reply_text("⬇️ Smaller")
    else:
        await update.message.reply_text("🎉 Correct!")
        del players[user_id]

bot.add_handler(CommandHandler("start", start))
bot.add_handler(MessageHandler(filters.TEXT, handle))

@app.route("/")
def home():
    return "OK"

@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot.bot)
    bot.update_queue.put_nowait(update)
    return "ok"

if name == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
