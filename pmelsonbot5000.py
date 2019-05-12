#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tweepy
import yaml
import re
import csv
from datetime import datetime, timedelta

start_date = datetime.today() - timedelta(days=1)
end_date = datetime.today()

def ioc_csv(ioc_data):
    """
    ioc_csv() serves to take a list of lists from the extract() function
    and turn it into a csv file that can be more easily ingested by automated
    tools.
    """

    top_row = ['malware/attack_tool', 'url', 'hash', 'c2']

    with open('scumfeed.csv', 'a') as fp:
        wr = csv.writer(fp)
        wr.writerow(top_row)
        for list in ioc_data:
            wr.writerow(list)
            

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
    
    return ioc_list
    

def main():

    with open('conf.yaml', 'r') as f:
        conf_data = yaml.safe_load(f)

    auth = tweepy.OAuthHandler(conf_data['consumer_key'], conf_data['consumer_secret'])
    auth.set_access_token(conf_data['access_token'], conf_data['access_token_secret'])

    api = tweepy.API(auth)

    twitter_raw = tweepy.Cursor(api.user_timeline, id="scumbots", since=start_date, until=end_date, tweet_mode='extended').items()
    
    twitter_formatted = extract(twitter_raw)
    
    csv_twitter_formatted = ioc_csv(twitter_formatted)


if __name__ == "__main__":
    main()
