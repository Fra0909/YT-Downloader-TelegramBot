import logging
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import regex as re
import downloader

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
yt = downloader
pattern = '^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$'

def help(update, context):
    update.message.reply_text("Send a youtube link and I will send you the video!")


def echo(update, context):
    if re.match(pattern, update.message['text']):
        print("Starting download of {} from {} ({})".format
              (update.message['text'],
               update.message['chat']['id'],
               update.message['chat']['username']))

        video = yt.main(update.message['text'])
        if video:
            info = video[1]
            try:
                with open(video[0], 'rb') as f:
                    update.message.reply_video(f, 'rb', caption=
                    'Title: {}\n'
                    'Duration: {}\n'
                    'Views: {}\n'
                    'Author: {}\n'
                    'Posted on: {}'.format(info['title'], info['length'], info['views'], info['author'],
                                           info['publish_date']))
            finally:
                os.remove(video[0])
                return
        print("Download aborted. Could not find a suitable file size.")
        update.message.reply_text(
            "The file size is too big. Telegram does not allow bots to send files larger than 50MB."
            "Try with a shorter video.\n A feature to split the videos in more parts will be implemented soon.")
        return
    update.message.reply_text("You must send a youtube link!")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater("TOKEN", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Handles /help command
    dp.add_handler(CommandHandler("help", help))

    #Handles every other message -- will change this
    dp.add_handler(MessageHandler(Filters.text, echo))


    # Error logging
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()