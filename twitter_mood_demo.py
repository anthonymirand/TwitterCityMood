#!/usr/bin/env python2.7

import os
import pytz
from datetime import datetime
import logging, json, csv

from requests_oauthlib import OAuth1Session
from requests.exceptions import Timeout, ConnectionError

from third_party.twitter_emotion_recognition.emotion_predictor import EmotionPredictor


class TwitterMood():
  search_url  = 'https://api.twitter.com/1.1/search/tweets.json?' \
                'q=lang%3Aen&result_type=recent&geocode={},{}&count=500'
  post_url    = 'https://api.twitter.com/1.1/statuses/update.json?'
  recent_url  = 'https://api.twitter.com/1.1/statuses/user_timeline.json?' \
                'screen_name={}&count=1'

  emotions = { 'Anger'    : 'angry',
               'Disgust'  : 'disgusted',
               'Fear'     : 'afraid',
               'Joy'      : 'happy',
               'Sadness'  : 'sad',
               'Surprise' : 'surprised' }

  current_directory = os.path.dirname(os.path.realpath(__file__))
  info_file         = '{}/info.json'.format(current_directory)
  log_error_file    = '{}/logs/error.log'.format(current_directory)
  history_file      = '{}/logs/history.log'.format(current_directory)
  history_all_file  = '{}/logs/history_all.log'.format(current_directory)

  logging.basicConfig(filename=log_error_file,
                      level=logging.ERROR,
                      format='%(asctime)s %(message)s')

  def __init__(self):
    with open(self.info_file, 'r') as file:
      info = json.loads(file.read())
    self.username     = info['username']
    self.coordinates  = info['coordinates']
    self.radius       = info['radius']
    self.city         = info['city']
    self.time_zone    = pytz.timezone(info['zone'])
    self.current_time = datetime.now(self.time_zone).strftime('%m/%d/%Y %H:%M')
    self.twitter = OAuth1Session(client_key=info['consumer_key'],
                            client_secret=info['consumer_secret'],
                            resource_owner_key=info['access_token'],
                            resource_owner_secret=info['access_secret'])

    self.tweets = self._get_tweets()
    self.emotion_count = self._analyze_tweets()
    self.mood = self._get_mood()
    self.last_mood = self._get_last_mood()

  def _get_tweets(self):
    r = self.twitter.get(url=self.search_url.format(self.coordinates, self.radius))
    if r.status_code == 200: # if successful
      tweets = [ status.get('text') for status in r.json().get('statuses') ]
    else:
      tweets = []
      logging.error(r.reason)
    return tweets if 0 < len(tweets) else []

  def _analyze_tweets(self):
    if len(self.tweets) == 0:
      return { emotion : 0 for emotion in self.emotions.keys() }

    model = EmotionPredictor(classification='ekman',
                             setting='ml',
                             use_unison_model=True)
    probabilities = model.predict_probabilities(self.tweets)
    return { emotion : sum(probabilities[emotion] / len(probabilities[emotion]))
             for emotion in self.emotions.keys() }

  def _get_mood(self):
    return self.emotions[ max(self.emotion_count, key=self.emotion_count.get) ]

  def _get_last_mood(self):
    r = self.twitter.get(url=self.recent_url.format(self.username))
    if r.status_code == 200: # if successful
      last_mood = r.json()[0]['text'].split()[-1]
    else:
      last_mood = None
      logging.error(r.reason)
    return last_mood if last_mood is not None else None

  def check_mood(self):
    combined = { key : self.emotion_count[key]
                 for key in sorted(self.emotion_count.keys()) }
    from pprint import pprint
    pprint(combined)

  def _post_mood(self):
    data = { 'status' : '{} is currently feeling {}'.format(self.city, self.mood) }
    try:
      r = self.twitter.post(url=self.post_url, data=data)
      if r != 200:
        logging.error(r.reason)
    except (ConnectionError, Timeout):
      time.sleep(60 * 2)
      r = self.twitter.post(url=self.post_url, data=data)

  def _write_file(self, mood_change):
    if mood_change:
      with open(self.history_file, 'aw') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerow([ self.city, self.current_time, self.mood ])

    with open(self.history_all_file, 'aw') as file:
      writer = csv.writer(file, delimiter=',')
      entries = [ self.emotion_count[key]
                  for key in sorted(self.emotion_count.keys()) ]
      writer.writerow([ self.city, self.current_time ] + entries)

if __name__ == '__main__':
  TwitterMood().check_mood()
