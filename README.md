Twitter: City Mood
===

## How is your city feeling?
### This python script will analyze tweets and tell you!

# Implementation
The script gathers tweets from a given location and counts the number of emotion-bearing words. After an hour, it tweets the emotion with the highest count (if the previous mood was different). You can see my example of the script in action in Los Angeles, CA at [@LosAngelesMood](http://www.twitter.com/LosAngelesMood).

# How to Install
The script utilizes the [requests](http://docs.python-requests.org/en/latest/) library: primarily requests and requests_oauthlib. If you do not already have this installed, you can run the command "pip install requests" in your command line/terminal of choice.

First, you will need to set up a [twitter account](https://twitter.com/signup) for the mood to be posted. Then, create a twitter app [here](https://apps.twitter.com/app/new) with your newly-created account. You will need to authorize this app to post to your account, which may require email verification and a phone number. Next, follow the instructions [here](https://dev.twitter.com/oauth/overview/application-owner-access-tokens) to create the OAuth tokens for your app.

Next, you will need to download this repository onto your computer. Github gives you two options to do so: cloning (through git) or downloading as a compressed file. Open city_mood_twitter.py in a text editor. In order for your Twitter account to analyze tweets in the location of your choice, locate the code at the top of the file that looks like this:

```
# FILL IN INFORMATION BELOW
DIRECTORY = '' #DIRECTORY OF twitter_city_sentiment
API_KEY = '' #CONSUMER KEY
API_SECRET = '' #CONSUMER SECRET
TOKEN_KEY = '' #ACCESS TOKEN
TOKEN_SECRET = '' #ACCESS TOKEN SECRET
LOCATION = '' #LATITUDE/LONGITUDE
RADIUS = '' #RADIUS
```

The space between each of those single quotes needs to be filled by the appropriate value. The first is the location where you downloaded this repository, e.g. `'/User/You/city_mood_twitter'`. The next four are authorization tokens that you will get from creating a Twitter app. The sixth is the geographic coordinates of the center of your city, e.g. `'34.0500,-118.2500'`. Finally, you'll need to enter the approximate radius of your city, e.g. `'1mi'`; to find an accurate radius, you can use the resource [here](http://www.freemaptools.com/radius-around-point.htm).

Lastly, you may want to set up Cron to run this script automatically. Cron jobs can be created by typing `crontab -e` into your terminal shell, and editing the file to include a new line with `00 * * * * python <path to downloaded repository>/city_mood_twitter.py`. In this case, the script will be run every hour on the hour. To set your own custom run time, you can read the [Cron quick reference guide](http://www.adminschoice.com/crontab-quick-reference).
