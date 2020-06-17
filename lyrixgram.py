import json
import requests
import logging
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

# global variables
musixmach_apikey = 'a1bfde9259fbb50d5022a3f6bee13bbe'
bot_token = '1218730927:AAE661Zx0OonH1gEx-DJNm3ZASP0MUPNsvA'
#bot_chatID = '1273304940'

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def hello(update, context):
    """Say hello."""
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))

def findLyrics(update, context):
    """Search text in the song title or artist name or lyrics. """
    global musixmach_apikey

    text = update.message.text
    text = text.replace('/search', '') # remove command from text
    if text == '' or text == ' ':
        update.message.reply_text('{}, enter a text to search'.format(update.message.from_user.first_name))
    else:
        response = requests.get(f'http://api.musixmatch.com/ws/1.1/track.search?apikey={musixmach_apikey}&q={text}&s_track_rating=desc&page=1&page_size=5')
        results = response.json()

        n = 0
        for t in results["message"]["body"]["track_list"]:
            n += 1
            if n == 1: #best result
                update.message.reply_text(f'Best result\n {n}: {t["track"]["track_name"]} - {t["track"]["artist_name"]} [{t["track"]["track_share_url"]}]')    
            else:
                update.message.reply_text(f'{n}: {t["track"]["track_name"]} - {t["track"]["artist_name"]}')
            

        #total match founds
        update.message.reply_text(f'Results: {n} / {results["message"]["header"]["available"]}')

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    global bot_token

    updater = Updater(bot_token, use_context=True)

    sg = updater.dispatcher

    sg.add_handler(CommandHandler('hello', hello))
    sg.add_handler(CommandHandler('search', findLyrics))

    sg.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()