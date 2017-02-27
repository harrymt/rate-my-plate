# Rate My Plate

Identify the environmental impact of food.

Developed for the [CSSBristol](cssbristol.co.uk) Boeing Hackathon.


## Development Setup

### Dependancies

- Install [Python](https://www.python.org/)
- Install [Pip](https://pypi.python.org/pypi/pip)

### Setup

- Clone repo `git clone https://github.com/harrymt/boeing-hackathon.git`
- Navigate to the directory `cd boeing-hackathon`
- Run `pip install -r requirements.txt` to install all Python dependancies
- Run the web server locally by running `python application.py`

### API Credentials
- Create your own file 'credentials.py' with a consumer_key, consumer_secret, access_token, and access_token_secret, which you can generate via the Twitter Application Management (https://apps.twitter.com)

```python
# credentials.py

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''
```

### Server Side Extra Setup

*Clone the Repo*

- `git clone https://github.com/harrymt/boeing-hackathon.git`
- Then `git pull` whenever there are changes

*Setup a Cron Job*

- `crontab -e` to show the list of cron jobs.
- Then add `* * * * * python twitterbot.py` to the cronfile.
- Then add `crontab -l` to check and see if it worked


### Technologies used

- [Python](https://www.python.org/)
- [Flask](flask.pocoo.org)
- [Tweepy](https://github.com/tweepy/tweepy)
- Hosted on [AWS](https://aws.amazon.com/)


## Overview

Tweet an <strike>image</strike> recipe of food to our account, and we tweet back an environmental report.

### Tasks

- <strike>Image Recognition using Google API (Lukasz)</strike>
- Create Python Server (Harry)
- Making Twitter bot (Ellie)
- Find out environmental impact of food (Matt)
- Taking meal and turning them into ingredients (Gavin)
- Front End to show off the product (Gavin)

