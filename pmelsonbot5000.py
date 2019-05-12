#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tweepy
import yaml
from datetime import datetime, timedelta

def main():

    with open('conf.yaml', 'r') as f:
        conf_data = yaml.safe_load(f)

    auth = tweepy.OAuthHandler(conf_data['consumer_key'], conf_data['consumer_secret'])
    auth.set_access_token(conf_data['access_token'], conf_data['access_token_secret'])

    api = tweepy.API(auth)

    start_date = datetime.today() - timedelta(days=30)
    end_date = datetime.today()

    for tweet in tweepy.Cursor(api.user_timeline, id="scumbots", since=start_date, until=end_date, tweet_mode='extended').items():
        if str(tweet.created_at) >= str(start_date.strftime("%Y-%m-%d %H:%M:%S")):
            print(str(tweet.full_text))


if __name__ == "__main__":
    main()
