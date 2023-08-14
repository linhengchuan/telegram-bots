import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
import requests
import schedule
import time
from threading import Thread

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(10)
        print("loop")

def function_to_run():
    print("test")

if __name__ == "__main__":
    # Create the job in schedule.
    s = schedule.every().day.at("00:49", "Singapore").do(function_to_run)
    print(s.next_run)

    Thread(target=schedule_checker).start() 
