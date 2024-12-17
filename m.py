import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to handle /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Welcome! Send me a Terabox link to download the video.')

# Function to handle incoming messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    link = update.message.text
    if 'terabox.com' in link:
        await update.message.reply_text(f"Processing your request for: {link}")
        # Call the download function here
    else:
        await update.message.reply_text('Please send a valid Terabox link.')

# Main function to start the bot
def main() -> None:
    # Replace 'YOUR_TOKEN' with your bot's token
    app = ApplicationBuilder().token("7511374887:AAFrYbS9kE095NXVaq4lEyCSKHg0VBIM6r4").build()

    # Add command and message handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the Bot
    app.run_polling()

if __name__ == '__main__':
    main()
  
