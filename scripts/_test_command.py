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
    # cmd = [BotCommand("/start", "Start chatting with GoldMemo Bot."),
    #        BotCommand("/help", "GoldMemo can help to remind user with memo, weather alert."),
    #        BotCommand("/settings", ""),
    #         ]
    cmd = [BotCommand("/start", "Start chatting with SeaTurtle Bot."),
            BotCommand("/help", "SeaTurtle can give user weather alert."),
            BotCommand("/settings", "/weather to get weather alert."),
            BotCommand("/weather_current", "Current weather alert"),
            BotCommand("/weather_auto_start", "Start daily weather alert"),
            BotCommand("/weather_auto_stop", "Stop daily weather alert"),
            ]
    await bot.set_my_commands(cmd)

if __name__ == '__main__':
    goldmemo_bot = Bot("6010838341:AAGaPXhE1SWGZLkKYg_fM0B7KRQ2ePIiau0")
    seaturtle_bot = Bot("6690176337:AAEFKa9JLcRqzt5N6XBZncXIn1BMbgSFMdI")

    if platform.system()=='Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # asyncio.run(set_command(goldmemo_bot))
    # asyncio.run(get_command(goldmemo_bot))
    asyncio.run(set_command(seaturtle_bot))
    # asyncio.run(get_command(seaturtle_bot))

