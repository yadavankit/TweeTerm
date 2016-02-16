"""Usage: tweeterm [-h]
       tweeterm LOCATION

TweeTerm is a command line interface (cli) for checking out the Trending 
Twitter HashTags and News on the Terminal. Just add your city/location name
as an argument and let the feeds decorate your Terminal.

Arguments:
  LOCATION       Location for where Trending Tweets are to be displayed

Options:
  -h --help
"""
from bs4 import BeautifulSoup
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
import json
from  docopt import docopt
import urllib2

__version__ = 0.1

#Access Tokens and Consumer Keys etc.
ACCESS_TOKEN = '2256458881-2g9oxprPUrHrrPuzE71NBj1kLWJeid8M4ai7JfK'
ACCESS_SECRET = 'Aw8PfrU5Xr4U8IU7NlmIe5b4KkeSoBU7P5R6lOO8VLwmC'
CONSUMER_KEY = 'lqOPSXUtBbfDxQhP2uMKgwYxC'
CONSUMER_SECRET = 'e2kxtqTlQaKK1aNL1TPA2LLx7Rrc4FRlBLyFUdEWKX87sDSN7v'
oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

#Initiate Connection to Twitter API
twitter = Twitter(auth=oauth)

#List of Available Places
world_trends = twitter.trends.available(_woeid=1)
place_id_list = []

#Crawls a URL and gets WOEID for Area Name
def crawlAreaCode(areaName):
	urlToParse = "http://woeid.rosselliot.co.nz/lookup/" + areaName
	page = urllib2.urlopen(urlToParse).read()
	soup = BeautifulSoup(page, "html.parser")
	areaCode = soup.find("td", {"class": "woeid"}).contents[0]
	return areaCode

#Display a Tweet on Terminal
def display_tweet(tweet):
	print tweet['name']


#Get Trending Tweets for specific WOEID
def trending_tweets(place_id):
	trending = twitter.trends.place(_id = place_id)
	for tweet in trending[0]['trends']:
		display_tweet(tweet)


#Check if Trends available for that place or not
def check_availability(place_id):
	if(place_id in place_id_list):
		trending_tweets(place_id)
	else:
		print "Sorry, Twitter doesn't provide trending topics for this Area. Please Try another."

#Main Function
def main():

	#Populate Place ID List
	for places in world_trends:
		place_id_list.append(places['woeid'])

	#Take arguments from Terminal Command
	arguments = docopt(__doc__, version=__version__)
	area = crawlAreaCode(arguments['LOCATION'])
	check_availability(int(area))


#Execute main() block
if __name__ == '__main__':
	main()