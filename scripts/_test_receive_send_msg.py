import asyncio
import telegram


async def main():
    bot = telegram.Bot("6010838341:AAGaPXhE1SWGZLkKYg_fM0B7KRQ2ePIiau0")
    async with bot:
        print(await bot.get_me())

async def receive():
    bot = telegram.Bot("6010838341:AAGaPXhE1SWGZLkKYg_fM0B7KRQ2ePIiau0")
    async with bot:
        print((await bot.get_updates())[0])

async def send():
    bot = telegram.Bot("6010838341:AAGaPXhE1SWGZLkKYg_fM0B7KRQ2ePIiau0")
    async with bot:
        await bot.send_message(text='Hi there!', chat_id=282080591)
        
if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
    asyncio.run(receive())
    asyncio.run(send())
    