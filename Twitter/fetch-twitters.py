# Tweepy module written by Josh Roselin, documentation at https://github.com/tweepy/tweepy
# MySQLdb module written by Andy Dustman, documentation at http://mysql-python.sourceforge.net/MySQLdb.html
# GeoSearch crawler written by Chris Cantey, MS GIS/Cartography, University of Wisconsin, https://geo-odyssey.com
# MwSQLdb schema written with great assistance from Steve Hemmy, UW-Madison DoIT

from __future__ import unicode_literals
from datetime import date, datetime
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import time
import sqlite3
import random
import atexit

# Go to http://dev.twitter.com and create an app. 
# The consumer key and secret as well as the access_token and secret will be generated for you after you register with Twitter Developers
consumer_key = 'OySWfXhTOuWDET1TWzAlA'
consumer_secret = '8oJ9Bgb3NtGT0ZXaYwps7bL5VoeADhyBI0ehf46Lk4'
access_token = '218353243-rGtM0FYe3Y034KckJLK51SbygU2nRrW8LD7DCNl7'
access_token_secret = 'ajzGIDa3hDvM7uxxOcOmOHYP4TPrfH5SZt6C17u134vwb'

# Create your MySQL schema and connect to database, ex: mysql> SET PASSWORD FOR 'root'@'localhost' = PASSWORD('newpwd');
conn = sqlite3.connect('/Users/xinyu/Desktop/twitter.sqlite')

Coords = dict()
Place = dict()
PlaceCoords = dict()
XY = []
c = conn.cursor()

def save(conn):
	print "Closing"
	conn.close()

atexit.register(save, conn)

class StdOutListener(StreamListener):
	""" A listener handles tweets that are the received from the stream. 
	This is a basic listener that inserts tweets into MySQLdb.
	"""
	def on_status(self, status):
		print "Tweet Text: ", status.text
		text = status.text
		print "Time Stamp: ", status.created_at
		try:
			Coords.update(status.coordinates)
			XY = (Coords.get('coordinates'))  #Place the coordinates values into a list 'XY'
			print "X: ", XY[0]
			print "Y: ", XY[1]
		except:
			# Often times users opt into 'place' which is neighborhood size polygon
			# Calculate center of polygon
			Place.update(status.place)
			PlaceCoords.update(Place['bounding_box'])
			Box = PlaceCoords['coordinates'][0]
			XY = [(Box[0][0] + Box[2][0])/2, (Box[0][1] + Box[2][1])/2]
			print "X: ", XY[0]
			print "Y: ", XY[1] 
			pass
		# Comment out next 4 lines to avoid MySQLdb to simply read stream at console
		c.execute("INSERT INTO twitters VALUES (?, ?, ?, ?, ?)",
			(status.id_str,status.created_at,XY[0],XY[1],text))
		conn.commit()

	def on_error(self, status_code):
		print >> sys.stderr, 'Encountered error with status code:', status_code
		return True # Don't kill the stream

	def on_timeout(self):
		print >> sys.stderr, 'Timeout...'
		return True # Don't kill the stream

def main():
	listener = StdOutListener()    
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	stream = Stream(auth, listener)
	#Only records 'locations' OR 'tracks', NOT 'tracks (keywords) with locations'
	while True:
		try:
			# Call tweepy's userstream method
			# Use either locations or track, not both
			stream.filter(locations=[-125, 25, -65, 48]) # These coordinates are approximate bounding box around USA
			#stream.filter(track=['obama'])## This will feed the stream all mentions of 'keyword' 
			break
		except Exception, e:
			 # Abnormal exit: Reconnect
			 nsecs = random.randint(1, 10)
			 time.sleep(nsecs)            

if __name__ == '__main__':
	main()
				