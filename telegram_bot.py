import logging
import requests
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Constants
TELEGRAM_BOT_TOKEN = os.getenv('6822388482:AAH5CFDnDS8ALNyDBWcyB-mEUDLOVF-Qx6Y')
SHORTENER_API_URL = 'https://ez4short.xyz/api?api={SHORTENER_API_KEY}'
SHORTENER_API_KEY = os.getenv('S12b2d8281afa6d870f9b44bd0cba166704c7ea50')

# Function to check balance
def check_balance():
    headers = {
        'Authorization': f'Bearer {SHORTENER_API_KEY}'
    }
    response = requests.get(SHORTENER_API_URL, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return f"Your current balance is: {data['balance']}"
    else:
        return "Failed to retrieve balance. Please try again later."

# Command handler for '/balance'
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    balance_info = check_balance()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=balance_info)

# Main function to start the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the URL Shortener Bot! Use /balance to check your balance.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Use /balance to check your balance. More features coming soon!")

async def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('balance', balance))

    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
