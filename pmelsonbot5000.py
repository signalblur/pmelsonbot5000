#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tweepy
import yaml
import re
import csv
import time
import os.path
import logging
from datetime import datetime, timedelta

start_date = datetime.today() - timedelta(days=30)
end_date = datetime.today()

def ioc_csv(ioc_data):
    """
    ioc_csv() serves to take a list of lists from the extract() function
    and turn it into a csv file that can be more easily ingested by automated
    tools.
    """

    top_row = ['date_identified', 'implant_type', 'url', 'hash', 'c2']

    try:
        if os.path.isfile('scumfeed.csv'):
            os.system('rm scumfeed.csv') # Removing data older than 30 days
            with open('scumfeed.csv', 'a') as fp:
                csv.writer(fp).writerow(top_row)
                wr = csv.writer(fp)
                for d in ioc_data:
                    wr.writerow(d)            

    except Exception as e:
        print('CSV creator failure.')
        print(e)


def extract(data):
    """
    This function serves to extract fields from the tweet to make them easily parsable.
    """

    ioc_list = []
    pattern = '((?P<name>\S{1,}) found at (?P<url>\S{1,}) SHA256: (?P<hash>[a-zA-Z0-9]{1,}) C2: (?P<c2>\S{1,}))'

    try:
        for tweet in data:
            append_list = []
            if str(tweet.created_at) >= str(start_date.strftime("%Y-%m-%d %H:%M:%S")):
                if 'Dexter' in str(tweet.full_text):
                    print(tweet.full_text)
                elif 'Alina' in str(tweet.full_text):
                    print(tweet.full_text)
                elif 'Diamondfox' in str(tweet.full_text):
                    print(tweet.full_text)
                elif 'Infinity' in str(tweet.full_text):
                    print(tweet.full_text)
                elif 'TreasureHunter' in str(tweet.full_text):
                    print(tweet.full_text)
                else:
                    reg_data = re.search(pattern, str(tweet.full_text))
                    append_list.append(tweet.created_at)
                    append_list.append(reg_data.group('name'))
                    append_list.append(reg_data.group('url'))
                    append_list.append(reg_data.group('hash'))
                    append_list.append(reg_data.group('c2').replace('tcp://', '').replace('http://', '').replace('[', '').replace(']', ''))
                    ioc_list.append(append_list)

    except Exception as e:
        print('Regex Parser failer')
        print(e)

    return ioc_list


def main():
    """
    App grabs past 30 days from the @ScumBots twitter feed, parses
    the data and makes it easily parsed for common security tooling.
    """

    while True:
        try: # Authentication area.
            with open('conf.yaml', 'r') as f:
                conf_data = yaml.safe_load(f)

            auth = tweepy.OAuthHandler(conf_data['consumer_key'], conf_data['consumer_secret'])
            auth.set_access_token(conf_data['access_token'], conf_data['access_token_secret'])

            api = tweepy.API(auth)

        except Exception as e:
            print('Unable to authenticate.')
            print(e)

        try: # Data Collection and parsing
            twitter_raw = tweepy.Cursor(api.user_timeline, id="scumbots", since=start_date, until=end_date, tweet_mode='extended').items()

            twitter_formatted = extract(twitter_raw)

            ioc_csv(twitter_formatted)
            time.sleep(7200) # Sleeping for 2 hours

        except Exception as e:
            print('Data parsing error')
            print(e)


if __name__ == "__main__":
    main()
