import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from bs4 import BeautifulSoup

# Your bot's token
BOT_TOKEN = '7511374887:AAFrYbS9kE095NXVaq4lEyCSKHg0VBIM6r4'

# Function to handle /start command
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hello! Send me a TeraBox video link, and I'll download it for you.")

# Function to scrape TeraBox to get the direct download link
def get_terabox_download_link(url: str):
    try:
        # Send GET request to TeraBox page
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        
        # Use BeautifulSoup to parse the page and find the video download link
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Example: Assume the download link is in a specific tag (this will vary)
        download_link = soup.find('a', {'class': 'download'})  # Modify the selector as needed
        if download_link and 'href' in download_link.attrs:
            return download_link.attrs['href']
        return None
    except Exception as e:
        print(f"Error in scraping: {e}")
        return None

# Function to download video with progress tracking
def download_video(url: str, file_name: str, update: Update):
    try:
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))

        if total_size == 0:
            update.message.reply_text("Failed to fetch video. Try again.")
            return False

        # Write the content to the file with progress tracking
        with open(file_name, 'wb') as f:
            downloaded = 0
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    progress = int(downloaded * 100 / total_size)
                    update.message.reply_text(f"Downloading: {progress}% complete", quote=True)

        return True
    except Exception as e:
        print(f"Error in downloading: {e}")
        update.message.reply_text("Error downloading the video.")
        return False

# Function to handle video URL message
async def handle_message(update: Update, context: CallbackContext):
    video_url = update.message.text.strip()

    # Check if the URL is from TeraBox (simple check)
    if 'terabox' not in video_url.lower():
        await update.message.reply_text("Please send a valid TeraBox video link.")
        return

    # Get the actual download link (API or Scraping)
    download_url = get_terabox_download_link(video_url)

    if not download_url:
        await update.message.reply_text("Could not find a direct download link. Try another video.")
        return

    file_name = "downloaded_video.mp4"

    # Start downloading the video
    await update.message.reply_text("Starting download... Please wait.")
    success = download_video(download_url, file_name, update)

    if success:
        # Send the video to the user
        with open(file_name, 'rb') as video_file:
            await update.message.reply_video(video=video_file)
        os.remove(file_name)  # Remove the file after sending
    else:
        await update.message.reply_text("Failed to download the video.")

# Main function to set up the bot
async def main():
    # Create an Application object instead of Updater
    application = Application.builder().token(BOT_TOKEN).build()

    # Register handlers for commands and messages
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start polling to listen for messages
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
