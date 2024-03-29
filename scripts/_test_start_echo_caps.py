import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text.upper())
    
async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)
    
if __name__ == '__main__':
    application = ApplicationBuilder().token("6010838341:AAGaPXhE1SWGZLkKYg_fM0B7KRQ2ePIiau0").build()
    
    start_handler = CommandHandler('start', start) #type /start to call start function
    application.add_handler(start_handler)
    
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo) #filter out /command words from being echoed
    application.add_handler(echo_handler)
    
    caps_handler = CommandHandler('caps', caps) #type /caps word to get WORD as reply
    application.add_handler(caps_handler)
    
    application.run_polling()