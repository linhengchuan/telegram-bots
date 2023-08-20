import logging
import telegram
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
import requests
import schedule
from threading import Thread
import time
import asyncio
import sys

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

set_of_chat_id = set()
MORNING_BRAODCAST_TIME = "22:54"
TOKEN_ID = "6690176337:AAEFKa9JLcRqzt5N6XBZncXIn1BMbgSFMdI"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hi! I am a sea turtle!")

async def weather_auto_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    set_of_chat_id.add(update.effective_chat.id)
    text = f"Sg weather will be broadcasted everyday at {MORNING_BRAODCAST_TIME}"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def weather_auto_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    set_of_chat_id.discard(update.effective_chat.id)
    text = "Sg weather will stop broadcasting everyday."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def weather_now(update: Update, context: ContextTypes.DEFAULT_TYPE):
    twenty_four_hours_adr = "https://api.data.gov.sg/v1/environment/24-hour-weather-forecast"
    start_time = requests.get(twenty_four_hours_adr).json().get('items')[0]['periods'][0]['time']['start'][:16]
    end_time = requests.get(twenty_four_hours_adr).json().get('items')[0]['periods'][0]['time']['end'][11:16]
    region_weather = ""
    for k,v in requests.get(twenty_four_hours_adr).json().get('items')[0]['periods'][0]['regions'].items():
        region_weather += f"{str(k)}: {v}\n"
    text = f"{start_time}-{end_time}: \n{region_weather}"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def weather_now_24h(update: Update, context: ContextTypes.DEFAULT_TYPE):
    twenty_four_hours_adr = "https://api.data.gov.sg/v1/environment/24-hour-weather-forecast"
    text = ""
    for i in [0,1,2]:
        start_time = requests.get(twenty_four_hours_adr).json().get('items')[0]['periods'][i]['time']['start'][:16]
        end_time = requests.get(twenty_four_hours_adr).json().get('items')[0]['periods'][i]['time']['end'][11:16]
        region_weather = ""
        for k,v in requests.get(twenty_four_hours_adr).json().get('items')[0]['periods'][i]['regions'].items():
            region_weather += f"{str(k)}: {v}\n"
        text += f"{start_time}-{end_time}: \n{region_weather} \n"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def send():
    bot = telegram.Bot(TOKEN_ID)
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
    if sys.platform == "win32" and sys.version_info >= (3, 8, 0):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    s = schedule.every().day.at(MORNING_BRAODCAST_TIME, "Singapore").do(send_weather)
    print(s.next_run)
    Thread(target=schedule_checker).start() 

    application = ApplicationBuilder().token(TOKEN_ID).build()

    start_handler = CommandHandler('start', start) #type /start to call start function
    application.add_handler(start_handler)

    weather_handler_auto_start = CommandHandler('weather_auto_start', weather_auto_start)
    application.add_handler(weather_handler_auto_start)

    weather_handler_auto_end = CommandHandler('weather_auto_end', weather_auto_end)
    application.add_handler(weather_handler_auto_end)
    
    weather_handler_now = CommandHandler('weather_now', weather_now)
    application.add_handler(weather_handler_now)

    weather_handler_now = CommandHandler('weather_now_24h', weather_now_24h)
    application.add_handler(weather_handler_now)
    
    application.run_polling(poll_interval=5)