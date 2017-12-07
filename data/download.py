import sys
import time
from TwitterSearch import *

# See https://developer.twitter.com/ on how to get an API key.
key = ''
secret = ''
token = ''
access = ''

def get_university_data(university):
	print "University: "+university+"\n"+time.strftime("%A %Y-%m-%d %H:%M")
	search = TwitterSearch(key, secret, token, access)
	
	file = open(university+"-tweets.txt", "w")
	
	options = TwitterSearchOrder()
	options.set_language("en")
	options.set_keywords([university])
	options.set_include_entities(False)
	options.set_result_type("recent")
	
	x = 1
	try:
		for tweet in search.search_tweets_iterable(options):
			line = tweet['user']['screen_name'] + "\t" + tweet['text'].replace("\n"," ").replace("\t", " ") + "\n"
			file.write(line.encode('utf-8'))
			if x % 100 == 0:
				print "Wow! "+str(x)+" tweets!"
			x += 1
	except:
		print "Failed with "+sys.exc_info()[0]
	finally:
		file.close()
		print "\nOverall tweets downloaded for "+university+": "+str(x)
		print time.strftime("%A %Y-%m-%d %H:%M")
		print "\n\n"

get_university_data("@uofcincy")
get_university_data("@MIT")
get_university_data("@CarnegieMellon")
get_university_data("@Stanford")
get_university_data("@UCBerkeley")
get_university_data("@Harvard")
get_university_data("@XavierUniv")
get_university_data("@miamiuniversity")
get_university_data("@OhioState")
