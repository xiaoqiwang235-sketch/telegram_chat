import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    filters,
    ContextTypes,
)

BOT_TOKEN = "8118733635:AAE6PbjSZrfmUKTYIjUJURhuKe_itZIiyuk"

OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL_NAME = "qwen3:4b"


def ask_ollama(prompt):
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)

    data = response.json()

    return data["response"]


async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    user_message = update.message.text

    print("用户消息:", user_message)
    print("",update)

    # reply = ask_ollama(user_message)

    reply = "hello seven"

    await update.message.reply_text(reply)


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(
    MessageHandler(filters.TEXT, handle_message)
)

print("机器人启动中...")

app.run_polling()