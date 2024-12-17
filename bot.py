import os
import requests
from tqdm import tqdm
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Use your bot token here
TOKEN = '7511374887:AAFrYbS9kE095NXVaq4lEyCSKHg0VBIM6r4'

def download_file(url, filename):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    with open(filename, 'wb') as file:
        with tqdm(total=total_size, unit='B', unit_scale=True) as bar:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
                    bar.update(len(chunk))

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Send me the TeraBox video URL to download.")

async def download(update: Update, context: CallbackContext):
    url = ' '.join(context.args)
    if not url:
        await update.message.reply_text("Please provide a valid TeraBox video URL.")
        return

    await update.message.reply_text("Downloading video...")

    filename = "downloaded_video.mp4"
    try:
        download_file(url, filename)
        await update.message.reply_text("Download complete! Sending file...")
        with open(filename, 'rb') as f:
            await update.message.reply_video(f)
    except Exception as e:
        await update.message.reply_text(f"Error occurred: {e}")

def main():
    # Create the Application
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('download', download))

    # Run the bot
    application.run_polling()

if __name__ == "__main__":
    main()
