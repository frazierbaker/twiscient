#!/usr/bin/env python
from stanfordcorenlp import StanfordCoreNLP
import time
import json
import os
if os.environ.get("PARALLEL"):
	from pyspark import *
# Run the following on each cluster node:
# nohup java -mx4g edu.stanford.nlp.pipeline.StanfordCoreNLPServer 8195 &

def analyze(tweet):
	nlp = StanfordCoreNLP("http://localhost")
	response = nlp.annotate(tweet, {"annotators": "sentiment", "outputFormat":"json"})
	rjson = json.loads(response)
	#Sum sentiment scores:
	sentimentSum = 0
	for sentence in rjson["sentences"]:
		# 0 = very neg; 1 = neg; 2 = neutral; 3 = pos; 4 = very pos
		# -2 puts neutral at 0, increases intuitivity
		sentimentSum += int(sentence["sentimentValue"])-2
	#Average sentiment values:
	sentimentAvg = float(sentimentSum)/len(rjson["sentences"])
	# count will be useful in parallel reduce
	return { "sum": sentimentSum, "avg": sentimentAvg, "count": 1 }

def sequential_with_annotations(path):
	diriter = os.listdir(path)
	for file in diriter:
		if file[0] != "@":
			continue #skip stats and annotation files
		statsfh = open(path+"/stats-"+file,"w")
		annotfh = open(path+"/annotation-"+file,"w")
		fh = open(path+"/"+file, "r")
		stats = { "ss": 0, "sa": 0, "aa": 0, "as": 0, "count": 0}
		for line in fh:
			tweet = line.split("\t")[1]
			result = analyze(tweet)
			annotfh.write(str(result["sum"])+"\t")
			annotfh.write(str(result["avg"])+"\n")
			stats["ss"]+=result["sum"] # sum of sums
			stats["sa"]+=result["avg"] # sum of avgs
			stats["count"]+=1
		stats["aa"] = float(stats["sa"])/stats["count"] # avg of avgs
		stats["as"] = float(stats["ss"])/stats["count"] # avg of sums
		statsfh.write("AA\tAS\tSA\tSS\tCT\n")
		statsfh.write(str(stats["aa"])+"\t")
		statsfh.write(str(stats["as"])+"\t")
		statsfh.write(str(stats["sa"])+"\t")
		statsfh.write(str(stats["ss"])+"\t")
		statsfh.write(str(stats["count"])+"\n")
		# Close files
		annotfh.close()
		statsfh.close()
		fh.close()

def sequential(path):
	diriter = os.listdir(path)
	for file in diriter:
		if file[0] != "@":
			continue #skip stats and annotation files
		statsfh = open(path+"/stats-"+file,"w")
		fh = open(path+"/"+file, "r")
		stats = { "ss": 0, "sa": 0, "aa": 0, "as": 0, "count": 0}
		for line in fh:
			tweet = line.split("\t")[1]
			result = analyze(tweet)
			stats["ss"]+=result["sum"] # sum of sums
			stats["sa"]+=result["avg"] # sum of avgs
			stats["count"]+=1
		stats["aa"] = float(stats["sa"])/stats["count"] # avg of avgs
		stats["as"] = float(stats["ss"])/stats["count"] # avg of sums
		statsfh.write("AA\tAS\tSA\tSS\tCT\n")
		statsfh.write(str(stats["aa"])+"\t")
		statsfh.write(str(stats["as"])+"\t")
		statsfh.write(str(stats["sa"])+"\t")
		statsfh.write(str(stats["ss"])+"\t")
		statsfh.write(str(stats["count"])+"\n")
		# Close files
		statsfh.close()
		fh.close()
		
def parallel(path):
	sc = SparkContext("local", "Twiscient")
	diriter = os.listdir(path)
	for file in diriter:
		if file[0] != "@":
			continue #skip stats and annotation files
		# Parallelize inner loop
		statsfh = open(path+"/stats-"+file,"w")
		file = sc.textFile(path+"/"+file)
		
		# Here's where the magic happens:
		mapped = file.map(lambda line: analyze(line.split("\t")[1].encode('utf-8')))
		sums = mapped.reduce(lambda a,b: { "count": a["count"]+b["count"], "sum": a["sum"]+b["sum"], "avg": a["avg"]+b["avg"] })
		
		# Pull info out of reduce data structure
		stats = { "ss": sums["sum"], "sa": sums["avg"], "aa": sums["avg"]/sums["count"], "as": float(sums["sum"])/sums["count"], "count": sums["count"] }
		statsfh.write("AA\tAS\tSA\tSS\tCT\n")
		statsfh.write(str(stats["aa"])+"\t")
		statsfh.write(str(stats["as"])+"\t")
		statsfh.write(str(stats["sa"])+"\t")
		statsfh.write(str(stats["ss"])+"\t")
		statsfh.write(str(stats["count"])+"\n")
		# Close files
		statsfh.close()	

begin = time.time()
if (os.environ.get("PARALLEL")):
	parallel("./twitter-parallel")
elif (os.environ.get("SEQUENTIAL")):
	sequential("./twitter-sequential")
else:
	print "No environment variable detected."
	print "Running sequentially with annotations."
	print "Do not time.\n"
	sequential_with_annotations("./twitter")
	exit()
end = time.time()
print "Time: "+str(end-begin)+"s\n"
