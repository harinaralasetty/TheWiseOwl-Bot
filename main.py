import praw
import os
import random
import time
from flask import Flask
from threading import Thread
from config import *

client_id = os.environ['client_id']
client_secret = os.environ['client_secret']
username = os.environ['username']
password = os.environ['password']

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    username=username,
    password=password,
    user_agent='<wise owl bot>',
)

with open("quotes.txt", "r") as quotes_file:
  soothing_sayings = quotes_file.readlines()

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, I'm alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

if __name__ == "__main__":
    keep_alive()

    for comment in reddit.inbox.stream():
        print(comment.body)

        try:
            reply_text = f"{prefix_word}{random.choice(soothing_sayings)}"
            comment.reply(reply_text)
            print(f"Replied to {comment.author}")

        except praw.exceptions.RedditAPIException as e:
            if "RATELIMIT" in str(e):
                print("Rate limit exceeded.")
              
        finally: 
          # if enable_sleep:
          random_seconds = random.randint(min_seconds, max_seconds)
          print(f"Sleeping for {random_seconds} seconds...")

          for remaining_seconds in range(random_seconds, 0, -1):
              print(f"Remaining seconds: {remaining_seconds}", end='\r')
              time.sleep(1)
