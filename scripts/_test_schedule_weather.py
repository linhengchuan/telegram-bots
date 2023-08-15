import logging
import telegram
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
import requests
import schedule
from threading import Thread
import time
import asyncio

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

set_of_chat_id = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text.upper()=="WEATHER":
        four_days_adr = "https://api.data.gov.sg/v1/environment/4-day-weather-forecast"
        response = requests.get(four_days_adr)
        weather_text=response.json().get('items')[0].get('forecasts')[0].get('date') + ": " + response.json().get('items')[0].get('forecasts')[0].get('forecast')
        print(response.json().get('items')[0].get('forecasts')[0].get('date') + ": " + response.json().get('items')[0].get('forecasts')[0].get('forecast'))
        await context.bot.send_message(chat_id=update.effective_chat.id, text=weather_text)

async def weather_auto_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    set_of_chat_id.add(update.effective_chat.id)
    text = "Sg weather will be broadcasted every morning."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def weather_auto_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    set_of_chat_id.discard(update.effective_chat.id)
    text = "Sg weather will stop broadcasting every morning."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def send():
    bot = telegram.Bot("6010838341:AAGaPXhE1SWGZLkKYg_fM0B7KRQ2ePIiau0")
    four_days_adr = "https://api.data.gov.sg/v1/environment/4-day-weather-forecast"
    response = requests.get(four_days_adr)
    weather_text=response.json().get('items')[0].get('forecasts')[0].get('date') + ": " + response.json().get('items')[0].get('forecasts')[0].get('forecast')
    for chat_id in list(set_of_chat_id):
        async with bot:
            await bot.send_message(text=weather_text, chat_id=chat_id)

def send_weather():
    asyncio.run(send())

def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(45)

if __name__ == '__main__':

    s = schedule.every().day.at("08:00", "Singapore").do(send_weather)
    print(s.next_run)
    Thread(target=schedule_checker).start() 

    application = ApplicationBuilder().token("6010838341:AAGaPXhE1SWGZLkKYg_fM0B7KRQ2ePIiau0").build()

    start_handler = CommandHandler('start', start) #type /start to call start function
    application.add_handler(start_handler)

    weather_handler_auto_start = CommandHandler('weather_auto_start', weather_auto_start)
    application.add_handler(weather_handler_auto_start)

    weather_handler_auto_end = CommandHandler('weather_auto_end', weather_auto_end)
    application.add_handler(weather_handler_auto_end)
    
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), weather) #type weather into chat. Not cmd.
    application.add_handler(echo_handler)
    
    application.run_polling(poll_interval=30)