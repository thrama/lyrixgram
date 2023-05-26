import json
import requests
import logging
import random
from pathlib import Path
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler


# read settings
with open(Path('confs/settings.json'), 'r') as json_file:
    confs = json.load(json_file)

musixmach_apikey = confs['credentials']['musicxmatch_apikey']
bot_token = confs['credentials']['telegrambot_token']

# enable logging
# first line is: time, levelName, fileName, functionName, lineNumber, message
logging.basicConfig(filename="lyrixgram.log", format='%(asctime)s, %(levelname)s, %(filename)s, %(funcName)s(), %(lineno)d, %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


#
# LIBS #######################################################################
#

# showLogo ###################################################################
def showLogo(update):
    """Just shows the logo."""
    randomNumber = random.randint(1, 5)

    if randomNumber == 5:
        update.message.reply_text('<em>(powered by <a href="https://www.musixmatch.com/">musiXmatch</a>)</em>',
                                    parse_mode=ParseMode.HTML,
                                    disable_web_page_preview=True)


# showResults ################################################################
def showResults(update, results, text):
    """Shows the find results."""
    n = 0
    for t in results["message"]["body"]["track_list"]:
        n += 1
        if n == 1:  # best result
            update.message.reply_text('*** Best result')
            update.message.reply_text(f'{n}) <b>{t["track"]["track_name"]}</b> - {t["track"]["artist_name"]} (rate: {t["track"]["track_rating"]}) [ <a href="{t["track"]["track_share_url"]}">&gt;&gt</a> ]', parse_mode=ParseMode.HTML, disable_web_page_preview=False)
            update.message.reply_text('***')
        else:
            update.message.reply_text(f'{n}) <b>{t["track"]["track_name"]}</b> - {t["track"]["artist_name"]} (rate: {t["track"]["track_rating"]}) [ <a href="{t["track"]["track_share_url"]}">&gt;&gt</a> ]', parse_mode=ParseMode.HTML, disable_web_page_preview=True)

    # total match founds
    update.message.reply_text(f'Results for <i>{text}</i>: {n} / {results["message"]["header"]["available"]}', parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    showLogo(update)

    logger.info(f'Provided best results to user [{format(update.message.from_user.first_name)}]')  #log


# showLukyResults ################################################################
def showLukyResults(update, results):
    """Show results for command 'lucky'."""
    update.message.reply_text('*** Luckiest result')
    update.message.reply_text(f'<b>{results["message"]["body"]["track"]["track_name"]}</b> - {results["message"]["body"]["track"]["artist_name"]} [ <a href="{results["message"]["body"]["track"]["track_share_url"]}">&gt;&gt</a> ]', parse_mode=ParseMode.HTML, disable_web_page_preview=False)
    showLogo(update)

    logger.info(f'Provided lukiest result to user [{format(update.message.from_user.first_name)}]')  #log


# error ######################################################################
def error(update, context):
    """Log errors caused by Updates."""
    logger.warning(f'Update {update} caused error {context.error}')


#
# COMMANDS ###################################################################
#

# hello ######################################################################
def hello(update, context):
    """Say hello."""
    update.message.reply_text(f'Hello, {format(update.message.from_user.first_name)}!')
    logger.info(f'Said hello to user [{format(update.message.from_user.first_name)}]')  #log


# findAll ####################################################################
def findAll(update, context):
    """Search text in the song title or artist name or lyrics."""
    text = update.message.text
    text = text.replace('/search ', '')  # remove command from text
    if text in ('', ' '):
        update.message.reply_text(f'{format(update.message.from_user.first_name)}, enter a text to search')

    else:
        try:
            # connect to the API service
            response = requests.get(f'http://api.musixmatch.com/ws/1.1/track.search?apikey={musixmach_apikey}&q={text}&s_track_rating=desc&page=1&page_size={confs["view"]["max_items"]}')
            results = response.json()
            logger.debug(f'{results}')

        except requests.exceptions.HTTPError as errh:
            logger.error(f"An Http Error occurred: {repr(errh)}")

        except requests.exceptions.ConnectionError as errc:
            logger.error(f"An Error Connecting to the API occurred: {repr(errc)}")

        except requests.exceptions.Timeout as errt:
            logger.error(f"A Timeout Error occurred: {repr(errt)}")

        except requests.exceptions.RequestException as err:
            logger.error(f"An Unknown Error occurred: {repr(err)}")

        else:
            if results["message"]["header"]["status_code"] == 200:  # the request was successful
                showResults(update, results, text)

            # authentication error
            elif results["message"]["header"]["status_code"] == 401:
                update.message.reply_text('AUTH ERROR: Oops, something went wrong...')
                logger.debug(f'Authentication failed: {results}')

            # the usage limit has been reached
            elif results["message"]["header"]["status_code"] == 402:
                update.message.reply_text('LIMIT ERROR: Oops, something went wrong...')
                logger.debug(f'The usage limit has been reached: {results}')

            # system busy
            elif results["message"]["header"]["status_code"] == 503:
                update.message.reply_text('musiXmatch is a bit busy at the moment and your request can''t be satisfied.')
                logger.debug(f'The usage limit has been reached: {results}')

            # others status codes
            # list of status codes:
            # https://developer.musixmatch.com/documentation/status-codes
            else:
                update.message.reply_text('Oops, something went wrong...')
                logger.debug(f'Generic error: {results}')


# findByTitle #################################################################
def findByTitle(update, context):
    """Search text in the song title."""
    text = update.message.text
    text = text.replace('/title ', '')  # remove command from text
    if text in ('', ' '):
        update.message.reply_text('{}, enter a text to search'.format(update.message.from_user.first_name))

    else:
        try:
            # connect to the API service
            response = requests.get(f'http://api.musixmatch.com/ws/1.1/track.search?apikey={musixmach_apikey}&q_track={text}&s_track_rating=desc&page=1&page_size={confs["view"]["max_items"]}')
            results = response.json()
            logger.debug(f'{results}')

        except requests.exceptions.HTTPError as errh:
            logger.error(f"An Http Error occurred: {repr(errh)}")

        except requests.exceptions.ConnectionError as errc:
            logger.error(f"An Error Connecting to the API occurred: {repr(errc)}")

        except requests.exceptions.Timeout as errt:
            logger.error(f"A Timeout Error occurred: {repr(errt)}")

        except requests.exceptions.RequestException as err:
            logger.error(f"An Unknown Error occurred: {repr(err)}")

        else:
            if results["message"]["header"]["status_code"] == 200:  # the request was successful
                showResults(update, results, text)

            # authentication error
            elif results["message"]["header"]["status_code"] == 401:
                update.message.reply_text('AUTH ERROR: Oops, something went wrong...')
                logger.debug('Authentication failed: {results}')

            # the usage limit has been reached
            elif results["message"]["header"]["status_code"] == 402:
                update.message.reply_text('LIMIT ERROR: Oops, something went wrong...')
                logger.debug(f'The usage limit has been reached: {results}')

            # system busy
            elif results["message"]["header"]["status_code"] == 503:
                update.message.reply_text('musiXmatch is a bit busy at the moment and your request can’t be satisfied.')
                logger.debug(f'The usage limit has been reached: {results}')

            # others status codes
            # list of status codes:
            # https://developer.musixmatch.com/documentation/status-codes
            else:
                update.message.reply_text('Ops. Something were wrong...')
                logger.debug(f'Generic error: {results}')


# iamLucky ###################################################################
def iamLucky(update, context):
    """If you fill lucky..."""
    trackFind = False

    # loop until a track is found or the process obtain a blocking error
    while trackFind is False:
        try:
            # generate a random number to use as track id
            randomNumber = random.randint(1, 6000000)

            # connect to the API service
            response = requests.get(f'http://api.musixmatch.com/ws/1.1/track.get?apikey={musixmach_apikey}&commontrack_id={randomNumber}')
            results = response.json()
            logger.debug(f'{results}')

        except requests.exceptions.HTTPError as errh:
            logger.error(f"An Http Error occurred: {repr(errh)}")

        except requests.exceptions.ConnectionError as errc:
            logger.error(f"An Error Connecting to the API occurred: {repr(errc)}")

        except requests.exceptions.Timeout as errt:
            logger.error(f"A Timeout Error occurred: {repr(errt)}")

        except requests.exceptions.RequestException as err:
            logger.error(f"An Unknown Error occurred: {repr(err)}")

        else:
            if results["message"]["header"]["status_code"] == 200:  # the request was successful
                showLukyResults(update, results)
                trackFind = True

            # authentication error
            elif results["message"]["header"]["status_code"] == 401:
                update.message.reply_text('AUTH ERROR: Oops, something went wrong...')
                logger.debug(f'Authentication failed: {results}')
                break

            # the usage limit has been reached
            elif results["message"]["header"]["status_code"] == 402:
                update.message.reply_text('LIMIT ERROR: Oops, something went wrong...')
                logger.debug(f'The usage limit has been reached: {results}')
                break

            # system busy
            elif results["message"]["header"]["status_code"] == 503:
                update.message.reply_text('musiXmatch is a bit busy at the moment and your request can''t be satisfied.')
                logger.debug(f'The usage limit has been reached: {results}')
                break

            # others status codes
            # list of status codes:
            # https://developer.musixmatch.com/documentation/status-codes
            else:
                update.message.reply_text('Oops, something went wrong... :(')
                logger.debug(f'Generic error: {results}')
                break


#
# MAIN #######################################################################
#

# main #######################################################################
def main():
    """Start the bot."""
    updater = Updater(bot_token, use_context=True)

    updater.dispatcher.add_handler(CommandHandler('hello', hello))
    updater.dispatcher.add_handler(CommandHandler('search', findAll))
    updater.dispatcher.add_handler(CommandHandler('title', findByTitle))
    updater.dispatcher.add_handler(CommandHandler('lucky', iamLucky))

    updater.dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
