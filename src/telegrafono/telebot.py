from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler, filters
)

from .llm import request_llm, parse_llm_response


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.partition(' ')[2]
    print("requesting llm")
    thinking, remaining = parse_llm_response(request_llm(query))
    thinking = "thinking:\n" + thinking
    remaining = "remaining:\n" + remaining

    def chunk_text(text, chunk_size=3000):
        return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

    thinking_chunks = chunk_text(thinking)
    remaining_chunks = chunk_text(remaining)

    for chunk in thinking_chunks:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=chunk)
    for chunk in remaining_chunks:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=chunk)


def application_builder(app_token: str) -> ApplicationBuilder:
    application = ApplicationBuilder().token(app_token).build()
    start_handler = CommandHandler("start", start)
    chat_handler = CommandHandler("chat", chat, filters=filters.TEXT)

    application.add_handler(start_handler)
    application.add_handler(chat_handler)

    return application
