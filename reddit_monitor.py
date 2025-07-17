"""
Reddit Monitoring Module

Streams Reddit comments from selected subreddits and flags harmful or grooming content
using the keyword_sentiment_analysis.py engine.

Usage:
    python reddit_monitor.py
"""

import praw
from analysis import analyze_sentiment  # Sentiment engine from analysis.py

# Reddit API credentials (replace with your own)
REDDIT_CLIENT_ID = "YOUR_CLIENT_ID"
REDDIT_CLIENT_SECRET = "YOUR_CLIENT_SECRET"
REDDIT_USER_AGENT = "ChildPredatorDetectionBot/0.1 by YOUR_USERNAME"

# Subreddits to monitor (you can add more)
SUBREDDITS_TO_MONITOR = "teenagers+AskTeenGirls+AskTeenBoys"
SENTIMENT_TO_FLAG = "negative"

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

subreddit = reddit.subreddit(SUBREDDITS_TO_MONITOR)

def monitor_comments():
    print(f"🚨 Monitoring comments in r/{SUBREDDITS_TO_MONITOR}...\n")
    try:
        for comment in subreddit.stream.comments(skip_existing=True):
            if comment.author is None:
                continue  # Skip deleted users

            result = analyze_sentiment(comment.body)

            if result["sentiment"] == SENTIMENT_TO_FLAG:
                print("⚠️  Suspicious Comment Detected")
                print(f"👤 Author: u/{comment.author}")
                print(f"💬 Comment: {comment.body}")
                print(f"📊 Analysis: {result}")
                print(f"🔗 Link: https://reddit.com{comment.permalink}")
                print("-" * 80)
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped by user.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    monitor_comments()
