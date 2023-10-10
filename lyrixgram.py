import logging
import random
import json
import requests
from pathlib import Path
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler

# Enable logging
logging.basicConfig(
    filename="lyrixgram.log",
    format='%(asctime)s, %(levelname)s, %(filename)s, %(funcName)s(), %(lineno)d, %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Read settings
settings_file = Path('confs/settings.json')
with open(settings_file, 'r') as json_file:
    confs = json.load(json_file)

musixmatch_apikey = confs['credentials']['musicxmatch_apikey']
bot_token = confs['credentials']['telegrambot_token']

# Show logo
def show_logo(update):
    """Just shows the logo."""
    if random.random() < 0.2:  # Generates a 20% chance
        message = '<em>(powered by <a href="https://www.musixmatch.com/">musiXmatch</a>)</em>'
        update.message.reply_text(
            message,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )

# Show results
def show_results(update, results, text):
    """Shows the find results."""
    track_list = results["message"]["body"]["track_list"]
    count = len(track_list)

    if count > 0:
        update.message.reply_text('*** Best result')
        for index, track in enumerate(track_list):
            track_name = track["track"]["track_name"]
            artist_name = track["track"]["artist_name"]
            track_rating = track["track"]["track_rating"]
            track_url = track["track"]["track_share_url"]

            if index == 0:
                update.message.reply_text('***')

            update.message.reply_text(
                f'{index + 1}) <b>{track_name}</b> - {artist_name} (rate: {track_rating}) [ <a href="{track_url}">&gt;&gt</a> ]',
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=False
            )

        update.message.reply_text(
            f'Results for <i>{text}</i>: {count} / {results["message"]["header"]["available"]}',
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
    else:
        update.message.reply_text(f'No results found for <i>{text}</i>.')

    show_logo(update)
    logger.info(f'Provided best results to user [{update.message.from_user.first_name}]')  # Log

# Show lucky results
def show_lucky_results(update, results):
    """Shows the luckiest result."""
    track = results["message"]["body"]["track"]
    track_name = track["track_name"]
    artist_name = track["artist_name"]
    track_url = track["track_share_url"]

    update.message.reply_text('*** Luckiest result')
    update.message.reply_text(
        f'<b>{track_name}</b> - {artist_name} [ <a href="{track_url}">&gt;&gt</a> ]',
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=False
    )

    show_logo(update)
    logger.info(f'Provided luckiest result to user [{update.message.from_user.first_name}]')  # Log

# Error handler
def error_handler(update, context):
    """Log errors caused by Updates."""
    logger.warning(f'Update {update} caused error {context.error}')

# Hello command
def hello_command(update, context):
    """Say hello."""
    update.message.reply_text(f'Hello, {update.message.from_user.first_name}!')
    logger.info(f'Said hello to user [{update.message.from_user.first_name}]')  # Log

# Find all command
def find_all_command(update, context):
    """Search text in the song title, artist name, or lyrics."""
    text = update.message.text.replace('/search ', '').strip()

    logging.info(f'User input for find_all_command: {text}')  # Log

    if not text:
        update.message.reply_text(f'{update.message.from_user.first_name}, enter a text to search')
    else:
        try:
            # Connect to the API service
            response = requests.get(
                f'http://api.musixmatch.com/ws/1.1/track.search?apikey={musixmatch_apikey}&q={text}&s_track_rating=desc&page=1&page_size={confs["view"]["max_items"]}'
            )
            results = response.json()
            logger.debug(f'{results}')
        except requests.exceptions.RequestException as err:
            logger.error(f"An Error occurred: {repr(err)}")
        else:
            if results["message"]["header"]["status_code"] == 200:  # The request was successful
                show_results(update, results, text)
            else:
                error_message = 'Oops, something went wrong...'
                status_code = results["message"]["header"]["status_code"]
                if status_code == 401:
                    error_message = 'AUTH ERROR: Oops, something went wrong...'
                elif status_code == 402:
                    error_message = 'LIMIT ERROR: Oops, something went wrong...'
                elif status_code == 503:
                    error_message = 'musiXmatch is a bit busy at the moment and your request can\'t be satisfied.'
                update.message.reply_text(error_message)
                logger.debug(f'Error with status code {status_code}: {results}')

# Find by title command
def find_by_title_command(update, context):
    """Search text in the song title."""
    text = update.message.text.replace('/title ', '').strip()

    logging.info(f'User input for find_by_title_command: {text}')  # Log

    if not text:
        update.message.reply_text(f'{update.message.from_user.first_name}, enter a text to search')
    else:
        try:
            # Connect to the API service
            response = requests.get(
                f'http://api.musixmatch.com/ws/1.1/track.search?apikey={musixmatch_apikey}&q_track={text}&s_track_rating=desc&page=1&page_size={confs["view"]["max_items"]}'
            )
            results = response.json()
            logger.debug(f'{results}')
        except requests.exceptions.RequestException as err:
            logger.error(f"An Error occurred: {repr(err)}")
        else:
            if results["message"]["header"]["status_code"] == 200:  # The request was successful
                show_results(update, results, text)
            else:
                error_message = 'Oops, something went wrong...'
                status_code = results["message"]["header"]["status_code"]
                if status_code == 401:
                    error_message = 'AUTH ERROR: Oops, something went wrong...'
                elif status_code == 402:
                    error_message = 'LIMIT ERROR: Oops, something went wrong...'
                elif status_code == 503:
                    error_message = 'musiXmatch is a bit busy at the moment and your request can’t be satisfied.'
                update.message.reply_text(error_message)
                logger.debug(f'Error with status code {status_code}: {results}')

# I am lucky command
def iam_lucky_command(update, context):
    """If you feel lucky..."""
    track_found = False

    # Loop until a track is found or the process encounters a blocking error
    while not track_found:
        try:
            # Generate a random number to use as track ID
            random_number = random.randint(1, 6000000)

            # Connect to the API service
            response = requests.get(
                f'http://api.musixmatch.com/ws/1.1/track.get?apikey={musixmatch_apikey}&commontrack_id={random_number}'
            )
            results = response.json()
            logger.debug(f'{results}')
        except requests.exceptions.RequestException as err:
            logger.error(f"An Error occurred: {repr(err)}")
        else:
            if results["message"]["header"]["status_code"] == 200:  # The request was successful
                show_lucky_results(update, results)
                track_found = True
            else:
                error_message = 'Oops, something went wrong... :('
                status_code = results["message"]["header"]["status_code"]
                if status_code == 401:
                    error_message = 'AUTH ERROR: Oops, something went wrong...'
                elif status_code == 402:
                    error_message = 'LIMIT ERROR: Oops, something went wrong...'
                elif status_code == 503:
                    error_message = 'musiXmatch is a bit busy at the moment and your request can\'t be satisfied.'
                update.message.reply_text(error_message)
                logger.debug(f'Error with status code {status_code}: {results}')
                break

# Main function
def main():
    """Start the bot."""
    updater = Updater(bot_token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('hello', hello_command))
    dispatcher.add_handler(CommandHandler('search', find_all_command))
    dispatcher.add_handler(CommandHandler('title', find_by_title_command))
    dispatcher.add_handler(CommandHandler('lucky', iam_lucky_command))

    dispatcher.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
