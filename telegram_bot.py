from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8667033910:AAEcAqxzvRdlQd8qewzeqR-z2TEG_ag7ep8"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! the number guessing robot is ready.")

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
print("Bot is running...")

app.run_polling()