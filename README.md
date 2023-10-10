# LyrixGram Bot

LyrixGram is a Telegram bot that allows you to search for song lyrics using the [musiXmatch](https://www.musixmatch.com/) API. You can search by song title, artist name, or even lyrics. Additionally, the bot provides a "lucky" feature that randomly selects a song for you.

## Prerequisites

Before getting started, ensure that you have the following prerequisites in place:

- [Python](http://https://www.python.org/) - version 3.9.2
- `pip` package manager
- [python-telegram-bot](https://python-telegram-bot.org/) - Dependency 

## Installation

Follow these steps to install LyrixGram:

1. Follow these steps to install LyrixGram:

    ```bash
    git clone https://github.com/thrama/lyrixgram.git
    ```

2. Install the required dependencies by running:

    ```bash
    pip install -r requirements.txt
    ```

3. Create a `confs/settings.json` file and populate it with your API credentials for musiXmatch and your Telegram bot. The file structure should be as follows:
   
   ```json
   {
        "credentials": {
            "musicxmatch_apikey": "YOUR_MUSIXMATCH_API_KEY",
            "telegrambot_token": "YOUR_TELEGRAM_BOT_TOKEN"
        },
        "view": {
            "max_items": 10
        }
   }
   ```

Replace `YOUR_MUSIXMATCH_API_KEY` with your actual musiXmatch API key and `YOUR_TELEGRAM_BOT_TOKEN` with your Telegram bot token.

> **Note:** The bot will create a log in the `lyrixgram.log` file.

## Usage

To begin using LyrixGram, follow these steps:

1. To begin using LyrixGram, follow these steps:

   ```bash
   python lyrixgram.py
   ```

   If you want to run the script in the background, you can use this command:

   ```bash
   nohup python lyrixgram.py $
   ```

3. Start a conversation with the bot on Telegram.

4. Use the following commands to interact with the bot:

    - `/hello` - Say hello to the bot.
    - `/search <text>` - Search for songs by text (title, artist name, or lyrics).
    - `/title <text>` - Search for songs by title.
    - `/lucky` - Get a randomly selected song.

## Contributing

We welcome contributions from the community! If you encounter any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. For more details, refert to [LICENSE](LICENSE) file.
