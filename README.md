Twitter City Mood
===

## How is your city feeling? This python script will analyze tweets and tell you!

This script gathers tweets from a given location and analyzes the tweets using a trained recurrent neural network (RNN). It then tweets the emotion with the highest frequency (if the previous mood was different). You can see my example of this script in action in Los Angeles, CA at [@LosAngelesMood](http://www.twitter.com/LosAngelesMood).

### Implementation
This script makes use of the trained emotion models from [@nikicc's Twitter Emotion Recognition](https://github.com/nikicc/twitter-emotion-recognition). This project trained a recurrent neural network on tweets queried using Ekman's six basic emotions. Edits were made to make the scripts/models Python 2.7 compatible. More specific data, methods, and results can be seen in the following paper:

*Colnerič, N., & Demšar, J. (2018). Emotion Recognition on Twitter: Comparative Study and Training a Unison Model. IEEE Transactions on Affective Computing, PP (99), 1. https://doi.org/10.1109/TAFFC.2018.2807817*

### Configuration
Below are the some of required configuration variables in *info.json* to run the script above. You may want to look up the coordinates of your city of choice, and use a [radius finder](http://www.freemaptools.com/radius-around-point.htm) to find an accurate radius around your city.

```
{
  "username"    : "losangelesmood",
  "coordinates" : "33.988,-118.180",
  "radius"      : "19.263mi",
  "city"        : "Los Angeles",
  "zone"        : "US/Pacific",

  "consumer_key"    : "INSERT TWITTER CONSUMER KEY HERE",
  "consumer_secret" : "INSERT TWITTER CONSUMER SECRET HERE",
  "access_token"    : "INSERT TWITTER ACCESS TOKEN HERE",
  "access_secret"   : "INSERT TWITTER ACCESS SECRET HERE"
}
```

You will need to set up a [twitter account](https://twitter.com/signup) for the mood to be posted. Then, create a twitter app [here](https://apps.twitter.com/app/new) with your newly-created account. You will need to authorize this app to post to your account, which may require email verification and a phone number. Next, follow the instructions [here](https://dev.twitter.com/oauth/overview/application-owner-access-tokens) to create the necessary OAuth tokens for your app.

### Files and Folders:
* __*info.json*__: configuration file to setup location parameters and Twitter credentials.
* __*twitter_mood_demo.py*__: script that performs tweet emotion analysis and prints out the emotion frequencies.
* __*twitter_mood.py*__: script that performs tweet emotion analysis and tweets to the designated Twitter account.
* __*third_party/*__: contains trained RNN models via [Twitter Emotion Recognition](https://github.com/nikicc/twitter-emotion-recognition).
