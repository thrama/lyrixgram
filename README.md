# Lyrixgram

Telegram bot [@Lyrixgrambot](https://t.me/Lyrixgrambot) to search lyrics with [musiXmatch](https://www.musixmatch.com/).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on deploying the project on a live system.

### Prerequisites

[Telegram](https://telegram.org/) app is available on most devices.
[python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) library provides a pure Python interface for the Telegram Bot API.

A complete list of libs used is in the file `requirements.txt`.

### Installing

The first step is to create the file for the credentials. You have to make a JSON file in the /conf directory. The structure of the file is:

```
{
  "credentials": {
      "musicxmatch_apikey": <API key>,
      "telegrambot_token": <token>
  },
	"view": {
		"max_items": 5
	}
}
```

You also need to update the part of the code to load the settings:

```
# read settings
with open(Path('confs/settings.json'), 'r') as json_file:
  confs = json.load(json_file)
```

The script creates a log file called `lyrixgram.log`.

## User's Guide

* `/hello` - Say Hello!
* `/search` - Search any word in the song title or artist name or lyrics
* `/title` - Search any word in the song title
* `/lucky` - I fill lucky!

## Built With

* [Python](http://https://www.python.org/) - version 3.9.2
* [Visual Studio Code](https://code.visualstudio.com/)
* [python-telegram-bot](https://python-telegram-bot.org/) - Dependency 

## Versioning

We use [SemVer](http://semver.org/) for versioning. See the [tags on this repository](https://github.com/thrama/lyrixgram/tags) for available versions.

## Authors

* **Lorenzo Lombardi** - [GitHub](https://github.com/thrama)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
