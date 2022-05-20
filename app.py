from pymongo import MongoClient
from flask import Flask, render_template,request, jsonify,redirect,url_for
import pymongo
import tweepy
import pandas as pd
import praw
app = Flask(__name__)
@app.route('/')
def home():
    return render_template('home.html') 
@app.route('/twitter', methods=['POST'])
def twitter():
    if request.method =='POST':
        if request.form['submit_button'] == 'Scrape':
            key=request.form['Name']
            datadict=tweetScrape(key)
            db = MongoClient("")
            x = db["SOCIAL_DATA_MINING"]["Tweet_scrape"].insert_many(datadict)
            return render_template('home.html')
        elif request.form['submit_button'] == 'Post':
            key=request.form['Name']
            datadict=tweetPost(key)
            return render_template('home.html')
@app.route('/reddit', methods=['POST'])
def reddit():
    if request.method=='POST':
        if request.form['submit_button'] == 'Scrape':
            key=request.form['Name']
            datadict=redditScrape(key)
            db = MongoClient("")
            x = db["SOCIAL_DATA_MINING"]["Reddit_scrape"].insert_many(datadict)
            return render_template('home.html')
        elif request.form['submit_button'] == 'Post':
            key=request.form['Name']
            datadict=redditPost(key)
            return render_template('home.html')
    #data=barchart1()          
    #return render_template('Home.html',data=data)


def redditScrape(key):
    Client_ID=""
    Client_SECRET=""
    USER_AGENT=""
    USERNAME=''
    reddit = praw.Reddit(client_id='', client_secret='', user_agent='')
    posts = []
    ml_subreddit = reddit.subreddit(key)
    for post in ml_subreddit.hot(limit=100):
        posts.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])
    posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])
    posts.to_csv('file1.csv')
    df = pd.read_csv("file1.csv", usecols = ['title','score','id','url','num_comments','body'])
    df.reset_index(inplace=True)
    datadict = df.to_dict('records')
    return datadict

def redditPost(msg):
    reddit = praw.Reddit(client_id='',client_secret='',user_agent='',redirect_uri='http://localhost:8080',refresh_token='')
    subr = 'pythonsandlot'
    subreddit = reddit.subreddit(subr) # Initialize the subreddit to a variable
 
    title = msg
    selftext = msg
    
    d=subreddit.submit(title,selftext=selftext)

    return d









def tweetScrape(keyword):
    consumer_key = ""
    consumer_secret = ""
    access_token = ""
    access_token_secret = ""
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth,wait_on_rate_limit=True)
    text_query = keyword
    count = 150
    # Creation of query method using parameters
    tweets = tweepy.Cursor(api.search,q=text_query).items(count)
    
    # Pulling information from tweets iterable object
    tweets_list = [[tweet.created_at, tweet.id, tweet.text] for tweet in tweets]
    
    # Creation of dataframe from tweets list
    # Add or remove columns as you remove tweet information
    tweets = tweepy.Cursor(api.search, q=text_query).items(count)
    # Pulling information from tweets iterable 
    tweets_list = [[tweet.created_at, tweet.id, tweet.text, tweet.user, tweet.favorite_count] for tweet in tweets]
    # Creation of dataframe from tweets list
    tweets_df = pd.DataFrame(tweets_list)
    tweets_df.to_csv('file2.csv')
    df = pd.read_csv("file2.csv", usecols = ['0','2','3'])
    df.reset_index(inplace=True)
    datadict = df.to_dict('records')
    return datadict
def tweetPost(msg):
    consumer_key = ""
    consumer_secret = ""
    access_token = ""
    access_token_secret = ""
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    api.update_status(status =msg)
    return 1
if __name__ == "__main__":
    app.run()