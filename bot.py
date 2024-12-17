import os
import requests
from tqdm import tqdm
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

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

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Send me the TeraBox video URL to download.")

def download(update: Update, context: CallbackContext):
    url = ' '.join(context.args)
    if not url:
        update.message.reply_text("Please provide a valid TeraBox video URL.")
        return

    update.message.reply_text("Downloading video...")

    filename = "downloaded_video.mp4"
    try:
        download_file(url, filename)
        update.message.reply_text("Download complete! Sending file...")
        with open(filename, 'rb') as f:
            update.message.reply_video(f)
    except Exception as e:
        update.message.reply_text(f"Error occurred: {e}")

def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('download', download))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
