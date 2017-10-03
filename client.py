#!/usr/bin/env python3

import socket
import sys
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
from clientKeys.py import ckey, csec, atok, asec,  track, hashstr

host = '192.168.1.9'
port = 50000
size = 1024
s = None

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

except socket.error as message:
    if s:
        s.close()
    print("Unable to open the socket: " + str(message))
    sys.exit(1)

print('[Checkpoint 03] Listening for Tweets that contain:', hashstr)


class listener(StreamListener):

    def on_data(self, data):
        tweet_data = json.loads(data)
        tweet = tweet_data["text"]
        user = tweet_data["user"]["screen_name"]
        print('[Checkpoint 04] New Tweet:', tweet, '| User:', user)
        tweetstr = ''.join(tweet)
        tweetstr = tweetstr.replace(hashstr, '')
        print('[Checkpoint 05] Speaking question parsed for only Alphanumeric and Space characters:', tweetstr)
        #TODO make RPi speak

        print('[Checkpoint 06] Connecting to', host, 'on port', port)
        s.connect((host, port))
        print('[Checkpoint 08] Sending question:', tweetstr)
        s.send(tweetstr.encode())
        recvdata = s.recv(size)
        s.close()
        print('[Checkpoint 14] Received answer:', recvdata.decode())
        return(True)

    def on_error(self, status_code):
        print(status_code)


auth = OAuthHandler(ckey, csec)
auth.set_access_token(atok, asec)


twitStream = Stream(auth, listener())
twitStream.filter(track=track)


