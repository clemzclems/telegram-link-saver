import logging
import re
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CommandHandler, CallbackContext

# Your Telegram Bot Token
TOKEN = "7710191740:AAFrSQbt3jMTw3ZTCxTHpa6yDOeFpt_pE4M"

# File to store Canvas links
LINKS_FILE = "canvas_links.txt"

# Regular expression to detect Canvas links
CANVAS_REGEX = r"https?://canvas\.[\w.-]+/\S*"

# Enable logging
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

async def save_canvas_link(update: Update, context: CallbackContext):
    """Detects and saves Canvas links from messages."""
    user_message = update.message.text
    chat_id = update.message.chat_id

    # Search for Canvas links in the message
    canvas_links = re.findall(CANVAS_REGEX, user_message)
    
    if canvas_links:
        with open(LINKS_FILE, "a") as file:
            for link in canvas_links:
                file.write(link + "\n")
        
        response = "Canvas link saved successfully!"
    else:
        response = "No Canvas link detected."

    # Reply to the user
    await context.bot.send_message(chat_id=chat_id, text=response)

async def start(update: Update, context: CallbackContext):
    """Sends a welcome message when the bot starts."""
    await update.message.reply_text("Hello! Send me a Canvas link, and I'll save it.")

def main():
    """Main function to run the bot."""
    app = Application.builder().token(TOKEN).build()

    # Add command and message handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, save_canvas_link))

    # Start the bot
    logging.info("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()

