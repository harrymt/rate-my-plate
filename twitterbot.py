import tweepy
import time
from credentials import *
import urllib
from pyshorteners import Shortener

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
print("Bot started.")

shortener = Shortener("Tinyurl")
recent_id = 0
image = False
url = 'http://34.250.158.151:3000/meals?{}={}'
reply = '@{} here is the environmental impact of your meal: '

while True:
	for tweet in tweepy.Cursor(api.search, q='@ratemyplate_', include_entities=True).items():
		
		if(tweet.id>recent_id):

			try:

				username = tweet.user.screen_name
				formatted_reply = reply.format(username)
				if 'media' in tweet.entities:
					image = True
					image = tweet.entities['media'][0]
					media = image['media_url']
					formatted_reply += shortener.short(url.format('image', media))

				else:
				
					text = tweet.text[14:].replace(" ", "+")
					location = tweet.user.location
					formatted_reply += shortener.short(url.format('recipe', text))

					
				print(formatted_reply)

					# urllib.request.urlopen('http://34.250.158.151:3000/meals?recipe=' + text).read()
					# api.update_status('@' + username + ' here is your meal: ' + urllib.parse.quote_plus(str(tweet.id)), in_reply_to_status_id=tweet.id)
				api.update_status(formatted_reply, in_reply_to_status_id=tweet.id)
				print("Tweet received from ", username)

			except tweepy.TweepError as e:
				print(e.reason)

			except StopIteration:
				break

		recent_id = tweet.id
		print("Bot finished.")

	time.sleep(30)
