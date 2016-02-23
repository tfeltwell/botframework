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
def exmpSearch():
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

    ## Example bot built by Tom, 
    ## This will fetch tweets about Hastings (minus any celebs or other shit)
    ## then send them the crack addiction rates :-)
    ## Read this about building queries: https://dev.twitter.com/rest/public/search

    ## Get the PHE data from the database
    query = (19, 94, 9, "2011/12") # Your query values need to be in here, in order of query (as below)
    c.execute('SELECT count FROM Data WHERE indicator_id=? AND area_id=? AND parent_id=? AND date_info=?',query )
    crackNumber = c.fetchone()[0]
    myTweet = "Did you know that in 2011/12 there were "+str(crackNumber)+" people who used crack and or opiates in Hastings?"
    # print myTweet # Debugging - Show what tweet we've done made

    ## Checking of highest ID to avoid spam
    highestID = 0

    ## Do a Twitter search, iterate for each result
    search_results = twitter.search(q='hastings -spencer -max -NE', result_type='recent', count=10)
    for i, result in enumerate(search_results["statuses"]):

        ## This bit prints stuff so we can see what it's doing
        # print result.keys() # Debugging - This will show us all the data for each tweet
        print i+1,':'
        print 'This is their tweet:',result["text"]
        print 'This is their name and ID:',result["user"]["name"],result["user"]["id_str"]
        print 'This is the ID of their tweet',result["id"]

        ## Do the tweeting
        replyID = result["id"] # Get the ID of the tweet so we can reply to it
        # twitter.update_status(status=myTweet, in_reply_to_status_id=replyID)

        # Check to store the highest ID
        if replyID > highestID:
            highestID = replyID

    print "Sleeping for 5 minutes now"
    time.sleep(300) # Sleep for 5 minutes

##############