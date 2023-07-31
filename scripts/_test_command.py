import logging
from telegram import Update, BotCommand
from telegram import Bot
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
import asyncio
import platform


async def get_command(bot):
    cmd = await bot.get_my_commands()
    print(cmd)

async def set_command(bot):
    cmd = [BotCommand("/start", "Start chatting with goldbot."),
           BotCommand("/help", "Goldbot can help to remind user with memo, weather alert."),
           BotCommand("/settings", "/weather to get weather alert."),
            ]
    await bot.set_my_commands(cmd)

if __name__ == '__main__':
    bot = Bot("6010838341:AAGaPXhE1SWGZLkKYg_fM0B7KRQ2ePIiau0")
    if platform.system()=='Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # asyncio.run(set_command(bot))
    asyncio.run(get_command(bot))

