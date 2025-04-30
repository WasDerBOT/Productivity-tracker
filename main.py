import asyncio
from telegram import ReplyKeyboardMarkup
import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler
from config import BOT_TOKEN
from datetime import datetime
from datetime import date as dt
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


async def echo(update, context):
    await update.message.reply_text("Я получил сообщение " + update.message.text)


async def start(update, context):
    reply_keyboard = [['/Reminders', '/Projects']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_text("Welcome !", reply_markup=markup)


async def Reminders(update, context):
    reply_keyboard = [['/Set', '/Change'],
                      ['/Check']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_text("Choose your option ", reply_markup=markup)


async def Projects(update, context):
    reply_keyboard = [['/Reminders', '/Projects']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_text("Welcome !", reply_markup=markup)


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    text_handler = MessageHandler(filters.TEXT, echo)
    application.add_handler(text_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
