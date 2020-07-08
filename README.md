# Lyrixgram 0.1.1

Telegram bot [@Lyrixgrambot](https://t.me/Lyrixgrambot) to search lyrics with [musiXmatch](https://www.musixmatch.com/).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

[Telegram](https://telegram.org/) app is available on the majority of devices.

### Installing

The first step needed to do is create the file for the credentials. You have to create a JSON file in the /conf directory. The structure of the file is:

```
{
	"credentials": {
		"musicxmatch_apikey": <API key>,
		"telegrambot_token": <token>
	}
}
```

You also need to update the parte of the code to load the credential:
```
# set credentials
with open(Path('confs/credentials.json'), 'r') as json_file:
  confs = json.load(json_file)
musixmach_apikey = confs['credentials']['musicxmatch_apikey']
bot_token = confs['credentials']['telegrambot_token']
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Python](http://https://www.python.org/)
* [Visual Studio Code](https://code.visualstudio.com/)
* [python-telegram-bot](https://python-telegram-bot.org/) - Dependency 

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/thrama/lyrixgram/tags). 

## Authors

* **Lorenzo Lombardi** - [GitHub](https://github.com/thrama)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
