from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler, filters
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.partition(' ')[2] 
    await context.bot.send_message(chat_id=update.effective_chat.id, text=query)


def application_builder(app_token: str) -> ApplicationBuilder:
    application = ApplicationBuilder().token(app_token).build()
    start_handler = CommandHandler("start", start)
    chat_handler = CommandHandler("chat", chat, filters=filters.TEXT)

    application.add_handler(start_handler)
    application.add_handler(chat_handler)

    return application
