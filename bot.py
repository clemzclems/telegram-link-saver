import logging
import re
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from telegram.request import HTTPXRequest
from flask import Flask, request

# Set up Flask app
app = Flask(__name__)

# Your Telegram Bot Token from Render environment variables
TOKEN = os.getenv("7710191740:AAFrSQbt3jMTw3ZTCxTHpa6yDOeFpt_pE4M")

# File to store Canvas links
LINKS_FILE = "canvas_links.txt"
CANVAS_REGEX = r"https?://canvas\.[\w.-]+/\S*"

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# Telegram request with timeout
request = HTTPXRequest(read_timeout=30, connect_timeout=30)
app_bot = Application.builder().token(TOKEN).request(request).build()

async def save_canvas_link(update: Update, context: CallbackContext):
    user_message = update.message.text
    chat_id = update.message.chat_id

    canvas_links = re.findall(CANVAS_REGEX, user_message)
    
    if canvas_links:
        with open(LINKS_FILE, "a") as file:
            for link in canvas_links:
                file.write(link + "\n")
        response = "Canvas link saved successfully!"
    else:
        response = "No Canvas link detected."

    await context.bot.send_message(chat_id=chat_id, text=response)

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hello! Send me a Canvas link, and I'll save it.")

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    app_bot.process_update(Update.de_json(request.get_json(force=True), app_bot))
    return "OK", 200

def main():
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, save_canvas_link))
    logging.info("Bot is ready and webhook set!")
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    main()
