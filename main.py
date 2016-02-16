from twython import *
import time, sqlite3

## INIT BLOCK ##

# Fill in your keys and secrets here!!
CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_KEY = ""
ACCESS_SECRET = ""
BOT_USERID = "000000000" #Find it at gettwitterid.com

twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)

# Connect to local PHE database
dbPath = "phe-data.sqlite"
conn = sqlite3.connect(dbPath, isolation_level=None)
c = conn.cursor()

################

## FUNCTIONS ##
def retweet(tweetID):
    twitter.retweet(id=tweetID)

def getIndicator(searchTerm):
    query = (searchTerm,) #Needs to be formatted as a tuple
    c.execute("SELECT * FROM Data WHERE indicator_id=?",query)
    results = c.fetchall()
    for i in results: #Iterate results
        print i 

## Code examples

# 1) Search twitter and retweet all results ##
def exmpRetweet(): 
    search_results = twitter.search(q='python', count=30)
    try:
        for tweet in search_results["statuses"]:
            retweet(tweet["id_str"])
    except TwythonError as e:
        print e

 # 2) Tweet a variable ##
def exmpTweet():

    myTweet = "Apologies for the spam, mucking around with the Twitter API!"
    try:
        twitter.update_status(status=myTweet)
    except TwythonError as e:
        print e

## 3) Search for something, do something with tweet ##
def exmpSearch(noTweets):
    search_results = twitter.search(q='programming', count=30)
    try:
        for count, tweet in enumerate(search_results['statuses']):
            print str(count),'-',tweet['text']
    except TwythonError as e:
        print e

## 4) Get followers for a user
def exmpFollowers():
    followers = []
    username = "dogsdoingthings"
    next_cursor = -1
    try:
        while(next_cursor):
            get_followers = twitter.get_followers_list(screen_name=username,count=200,cursor=next_cursor)
            for follower in get_followers["users"]:
                followers.append(follower["screen_name"].encode("utf-8"))
                next_cursor = get_followers["next_cursor"]
        print followers # Or do something else with them...
    except TwythonError as e:
        print e

## MAIN LOOP ##
# Keep running until killed
while(True):

    exmpFollowers()

    print "Sleeping for 5 minutes now"
    time.sleep(300) # Sleep for 5 minutes

##############