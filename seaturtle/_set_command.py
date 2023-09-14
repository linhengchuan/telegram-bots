import asyncio
import os
import platform
import sys

from telegram import Bot, BotCommand


if sys.platform == 'win32':
    token_file_path = os.path.dirname(
        os.path.abspath(__file__)) + "\\_token.txt"
    chat_id_file_path = os.path.dirname(
        os.path.abspath(__file__)) + "\\_chat_id.txt"
else:
    token_file_path = os.path.dirname(
        os.path.abspath(__file__)) + "/_token.txt"
    chat_id_file_path = os.path.dirname(
        os.path.abspath(__file__)) + "/_chat_id.txt"

try:
    with open(token_file_path, 'r') as file:
        TOKEN_ID = file.read()
except FileNotFoundError:
    print("The file does not exist.")


async def get_command(bot):
    cmd = await bot.get_my_commands()
    print(cmd)


async def set_command(bot):
    cmd = [BotCommand("/start", "Start chatting with SeaTurtle Bot."),
           BotCommand("/weather_now", "Current weather alert"),
           BotCommand(
        "/weather_now_24h",
        "Weather alert for the next 24hours"),
        BotCommand("/weather_auto_start", "Start daily weather alert"),
        BotCommand("/weather_auto_stop", "Stop daily weather alert"),
        BotCommand("/weather_auto_stop", "Stop daily weather alert"),
        BotCommand("/settings", "/weather to get weather alert."),
        BotCommand("/help", "SeaTurtle can give user weather alert."),
    ]
    await bot.set_my_commands(cmd)

if __name__ == '__main__':
    seaturtle_bot = Bot(TOKEN_ID)

    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(set_command(seaturtle_bot))
        # asyncio.run(get_command(seaturtle_bot))
