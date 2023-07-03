# LyrixGram Bot

LyrixGram is a Telegram bot that allows you to search for song lyrics using the [musiXmatch](https://www.musixmatch.com/) API. You can search by song title, artist name, or even lyrics. Additionally, the bot provides a "lucky" feature that randomly selects a song for you.

## Prerequisites

- [Python](http://https://www.python.org/) - version 3.9.2
- `pip` package manager
- [python-telegram-bot](https://python-telegram-bot.org/) - Dependency 

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/thrama/lyrixgram.git
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Create a `confs/settings.json` file and add your API credentials for musiXmatch and Telegram bot. The file should have the following structure:

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

> **Note:** The script creates a log in the file `lyrixgram.log`.

## Usage

1. Run the script:

    ```bash
    python lyrixgram.py
    ```

2. Start a conversation with the bot on Telegram.

3. Use the following commands to interact with the bot:

    - `/hello` - Say hello to the bot.
    - `/search <text>` - Search for songs by text (title, artist name, or lyrics).
    - `/title <text>` - Search for songs by title.
    - `/lucky` - Get a randomly selected song.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details