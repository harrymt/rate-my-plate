# Rate My Plate

Identify the environmental impact of food.

Developed for the [CSSBristol](cssbristol.co.uk) Boeing Hackathon.


## Development Setup

### Dependancies

- Install [Python](https://www.python.org/) *version: 3.5* (required for tensorflow)
- Install [Pip](https://pypi.python.org/pypi/pip)
- Make sure pip is updated `pip install --upgrade pip`


### Setup

- Clone repo `git clone https://github.com/harrymt/boeing-hackathon.git`
- Navigate to the directory `cd boeing-hackathon`
- Run `pip install -r requirements.txt` to install all Python dependancies
- Setup the Database `python db_setup.py`
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

*Setup a GitHook*

- Create a `pull.php` file with 1 line, `<?php exec('cd boeing-hackathon && git pull'); ?>`


### Technologies used

- [Python](https://www.python.org/)
- [Flask](flask.pocoo.org)
- [Tweepy](https://github.com/tweepy/tweepy)
- [TensorFlow](https://www.tensorflow.org)
- [Bit.ly](https://bit.ly)
- [Leaflet](http://leafletjs.com/)
- Hosted on [AWS](https://aws.amazon.com/)

## Overview

Tweet an <strike>image</strike> recipe of food to our account, and we tweet back an environmental report.

