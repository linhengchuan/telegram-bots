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
    cmd = [BotCommand("/start", "Start chatting with SeaTurtle Bot."),
            BotCommand("/weather_now", "Current weather alert"),
            BotCommand("/weather_now_24h", "Weather alert for the next 24hours"),
            BotCommand("/weather_auto_start", "Start daily weather alert"),
            BotCommand("/weather_auto_stop", "Stop daily weather alert"),
            BotCommand("/weather_auto_stop", "Stop daily weather alert"),
            BotCommand("/settings", "/weather to get weather alert."),
            BotCommand("/help", "SeaTurtle can give user weather alert."),
            ]
    await bot.set_my_commands(cmd)

if __name__ == '__main__':
    seaturtle_bot = Bot("6690176337:AAEFKa9JLcRqzt5N6XBZncXIn1BMbgSFMdI")

    if platform.system()=='Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(set_command(seaturtle_bot))
        # asyncio.run(get_command(seaturtle_bot))

