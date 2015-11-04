#!/usr/bin/env python

"""
	Python script for a Twitter Bot that pools tweets from a specified radius around
	a provided location, and counts the instances of emotion-bearing words. The emotion
	counts are compared to find the "most" tweeted emotion in the city, which is 
	posted to the Twitter account.
"""

__author__ = "Anthony Mirand"
__version__ = "0.1.0"
__email__ = "anthonypmirand@gmail.com"

import time
import os
import logging
from ast import literal_eval
from requests_oauthlib import OAuth1Session
from requests.exceptions import Timeout, ConnectionError

# FILL IN INFORMATION BELOW
DIRECTORY = '' #DIRECTORY OF twitter_city_sentiment
API_KEY = '' #CONSUMER KEY
API_SECRET = '' #CONSUMER SECRET
TOKEN_KEY = '' #ACCESS TOKEN
TOKEN_SECRET = '' #ACCESS TOKEN SECRET
LOCATION = '' #LATITUDE/LONGITUDE
RADIUS = '' #RADIUS


TWITTER = OAuth1Session(API_KEY,client_secret=API_SECRET,resource_owner_key=TOKEN_KEY,resource_owner_secret=TOKEN_SECRET)
logging.basicConfig(filename = DIRECTORY + '/mood.log', level = logging.ERROR, format = '%(asctime)s %(message)s')
SEARCH_URL = 'https://api.twitter.com/1.1/search/tweets.json?q=lang%3Aen&result_type=recent&geocode=' + LOCATION + ',' + RADIUS
POST_URL = 'https://api.twitter.com/1.1/statuses/update.json?'

def get_mood():
	tweets = []
	with open('emotion_dictionary.txt','r') as f: 	# LOADS KEYWORD DICTIONARY
		emotion_dictionary = literal_eval(f.read())
	counts = { key:0 for key in emotion_dictionary.keys() }
	while int(time.strftime('%M',time.localtime())) < 57:
		r = TWITTER.get(url = SEARCH_URL)
		if r.status_code == 200: 					# IF SUCCESSFUL
			for status in r.json().get('statuses'):
				tweets.append(status.get('text'))
		time.sleep(10)
		if r.status_code == 420: 					# IF BEING THROTTLED
			logging.error(r.reason)
		if r.status_code == 429: 					# IF EXCEDING REQUEST FREQUENCY
			logging.error(r.reason)
			time.sleep(60)
	for status in tweets: 							# COUNT FREQUENCY OF KEYWORDS
		for key in emotion_dictionary.keys():
			counts.update({key:counts.get(key) + len(set(status.lower().split()) & set(emotion_dictionary.get(key)))})
	if sum(counts.values()) == 0: 					# IF NO KEYWORDS
		return 'nothing'
	elif counts.values().count(counts.values()[0]) == len(counts.values()): #IF NO PREVALENT KEYWORDS
		return 'everything'
	else: 											# SORT COUNTS AND RETURNS KEY OF HIGHEST VALUE (MOST EXPRESSED EMOTION)
		return sorted([(counts.get(key),key) for key in counts])[-1][-1]

def post_mood():
	os.chdir(DIRECTORY)
	mood = get_mood()
	if not os.path.isfile('old_mood.txt'):
		with open('old_mood.txt','w') as f:
			f.write('')
	with open('old_mood.txt','r') as f:
		old_mood = f.read()
	if mood != old_mood:
		with open('old_mood.txt','w') as f:
			f.write(mood)
		data = { 'status':'[CITY] is currently feeling ' + mood } # CORRESPONDING CITY OF SENTIMENT SEARCH
		try:
			r = TWITTER.post(url=POST_URL,data=data)
			if r == 401: 							# IF AUTHORIZATION FAILS
				logging.error(r.reason)
			if r == 403: 							# IF FORBIDDEN
				logging.error(r.reason)
		except ConnectionError:
			time.sleep(120)
			r = TWITTER.post(url=POST_URL,data=data)
		except Timeout:
			time.sleep(120)
			r = TWITTER.post(url=POST_URL,data=data)
	else:
		pass

if __name__ == '__main__':
	post_mood()

