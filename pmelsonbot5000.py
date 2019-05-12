#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tweepy
import yaml
import re
from datetime import datetime, timedelta

start_date = datetime.today() - timedelta(days=1)
end_date = datetime.today()

def extract(data):
    """
    This function serves to extract fields from the tweet to make them easily parsable.
    """

    ioc_list = []
    pattern = '((?P<name>\S{1,}) found at (?P<url>\S{1,}) SHA256: (?P<hash>[a-zA-Z0-9]{1,}) C2: (?P<c2>\S{1,}))'
    
    for tweet in data:
        append_list = []
        if str(tweet.created_at) >= str(start_date.strftime("%Y-%m-%d %H:%M:%S")):
            reg_data = re.search(pattern, str(tweet.full_text))
            append_list.append(reg_data.group('name'))
            append_list.append(reg_data.group('url'))
            append_list.append(reg_data.group('hash'))
            append_list.append(reg_data.group('c2'))
            ioc_list.append(append_list)
    
    print(ioc_list)
    

def main():

    with open('conf.yaml', 'r') as f:
        conf_data = yaml.safe_load(f)

    auth = tweepy.OAuthHandler(conf_data['consumer_key'], conf_data['consumer_secret'])
    auth.set_access_token(conf_data['access_token'], conf_data['access_token_secret'])

    api = tweepy.API(auth)

    twitter_raw = tweepy.Cursor(api.user_timeline, id="scumbots", since=start_date, until=end_date, tweet_mode='extended').items()
    
    twitter_formatted = extract(twitter_raw)
        


if __name__ == "__main__":
    main()
