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
import os

if sys.platform=='win32':
    token_file_path = os.path.dirname(os.path.abspath(__file__)) + "\\_token.txt"
    chat_id_file_path = os.path.dirname(os.path.abspath(__file__)) + "\\_chat_id.txt"
else:
    token_file_path = os.path.dirname(os.path.abspath(__file__)) + "/_token.txt"
    chat_id_file_path = os.path.dirname(os.path.abspath(__file__)) + "/_chat_id.txt"

try:
    with open(token_file_path, 'r') as file:
        TOKEN_ID = file.read()
except FileNotFoundError:
    print("The file does not exist.")

try:
    with open(chat_id_file_path, 'r') as file:
        content = file.read()
        values = content.strip().split(', ')
        set_of_chat_id = set([int(i) for i in values if len(i)!=0])
        print(f"set_of_chat_id {set_of_chat_id}")
except FileNotFoundError:
    print("The file does not exist.")
except Exception as e:
    print("An error occurred:", e)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

MORNING_BRAODCAST_TIME = "23:00"

def update_chat_id():
    try:
        set_string = ', '.join(str(item) for item in set_of_chat_id)
        print(f"set_string: {set_string}")
        with open(chat_id_file_path, 'w') as file:
            file.write(set_string)
        print("Set written to file successfully.")
    except Exception as e:
        print("An error occurred:", e)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hi! I am a sea turtle!")

async def weather_auto_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    set_of_chat_id.add(update.effective_chat.id)
    update_chat_id()
    text = f"Sg weather will be broadcasted everyday at {MORNING_BRAODCAST_TIME}"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def weather_auto_stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    set_of_chat_id.discard(update.effective_chat.id)
    update_chat_id()
    text = "Sg weather will stop broadcasting everyday."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def weather_now(update: Update, context: ContextTypes.DEFAULT_TYPE):
    two_hours_adr = "https://api.data.gov.sg/v1/environment/2-hour-weather-forecast"
    response = requests.get(two_hours_adr)
    start_time = response.json().get('items')[0]['valid_period']['start'][:16]
    end_time = response.json().get('items')[0]['valid_period']['end'][11:16]
    region_weather = ""
    ls_region_weather = [i['area'] + ': ' + i['forecast'] + '\n' for i in response.json().get('items')[0]['forecasts']]
    for i in ls_region_weather:
        region_weather += i 
    text = f"{start_time}-{end_time}: \n{region_weather}"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def weather_now_24h(update: Update, context: ContextTypes.DEFAULT_TYPE):
    twenty_four_hours_adr = "https://api.data.gov.sg/v1/environment/24-hour-weather-forecast"
    response = requests.get(twenty_four_hours_adr)
    text = ""
    for i in [0,1,2]:
        start_time = response.json().get('items')[0]['periods'][i]['time']['start'][:16]
        end_time = response.json().get('items')[0]['periods'][i]['time']['end'][11:16]
        region_weather = ""
        for k,v in response.json().get('items')[0]['periods'][i]['regions'].items():
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

    weather_handler_auto_end = CommandHandler('weather_auto_stop', weather_auto_stop)
    application.add_handler(weather_handler_auto_end)
    
    weather_handler_now = CommandHandler('weather_now', weather_now)
    application.add_handler(weather_handler_now)

    weather_handler_now = CommandHandler('weather_now_24h', weather_now_24h)
    application.add_handler(weather_handler_now)
    
    application.run_polling(poll_interval=5)