from mpi4py import MPI
# Import csv to read files and arguments
import sys, getopt
# Import regular expressions to look for topics and mentions, json to parse tweet data
import re, json, operator,os
# Import numpy
import numpy as np
# Import Counter
from collections import Counter
# Import pprint
from pprint import pprint
# Import time
from time import process_time_ns 


def remove_trails(text):
	"""
	Remove unwanted trailing characters from json text
	text: line of json text
	"""

	text = text.rstrip() # remove trailing whitespace (\n)
	text = re.sub(r"(?<=}),?]?}?$", "", text) # remove unwanted trailing ',' ']' '}'

	return text


def parse_tweet(text):
	"""
	Parse for Tweet Data Dictionary in json text, under field "doc"
	text: line of json text
	"""

	try:
		data = json.loads(text)
		tweet = data["doc"]
	except json.decoder.JSONDecodeError: # illegal text
		tweet = {} 

	return tweet


def extract_hashtags(tweet):
	"""
	Extract hashtags from Tweet Data Dictionary and convert to lowercase
	tweet: Tweet Data Dictionary
	"""

	if not tweet:
		return []

	hashtags = tweet["entities"]["hashtags"]
	names = [tag["text"].lower() for tag in hashtags] # lowercased hashtag names (without #)

	return names


def extract_language(tweet):
	"""
	Extract language from Tweet Data Dictionary
	"""

	return tweet.get("lang", "")


class Tweet:
	"""Process line of json text for single tweet data"""

	def __init__(self, text):
		"""
		text: line of json text
		"""

		self.text = text

		# Tweet data
		text_clean = remove_trails(text)
		self.data = parse_tweet(text_clean)

		# Extract information
		self.hashtags = extract_hashtags(self.data)
		self.lang = extract_language(self.data) # language




def read_lines(filename, start, end):
	
	with open(filename) as f:
		f.seek(start)
		while f.tell() < end:  #returns the current position of the file read/write pointer within the file
			yield f.readline()


def count_hashtags_langs(filename, start, end):
	"""
	Count hashtags and languages in specific chunk of filename
	filename: json file containing tweet data (big file)
	start: byte position to read from (defaults to start of file)
	end: byte position to read to (defaults to end of file)
	"""

	htcounts = Counter() # hashtag counts
	langcounts = Counter() # language counts
	for text in read_lines(filename, start, end):
		tweet = Tweet(text)
		if not tweet.data: # badly formatted line
			continue

		htcounts.update(tweet.hashtags)
		langcounts[tweet.lang] += 1

	return htcounts, langcounts


def process_chunk(comm, filename, size, rank):
	#Break file into chunks and get processed
	
	filesize = os.path.getsize(filename)
	start = int(rank*filesize/size)
	end = int((rank+1)*filesize/size)

	htcounts, langcounts = count_hashtags_langs(filename, start, end)

	return htcounts, langcounts


def sum_counter(htcounts_all):
	# Sum up the values from different processes
	overall_count = Counter()
	for i in htcounts_all:
		overall_count.update(i)
	return overall_count


def main(argv):

	t1 = process_time()

	filename = read_arguments(argv)

	comm = MPI.COMM_WORLD
	rank = comm.Get_rank()
	size = comm.Get_size()
	htcounts, langcounts = process_chunk(comm, filename, size, rank)
		
	#Gather all processed data and send to rank 0
	htcounts_all = comm.gather(htcounts, root=0)
	langcounts_all = comm.gather(langcounts, root=0)
	
	#Rank 0 return the overall hashtag and languange counts
	if rank == 0:
		overall_htcounts = sum_counter(htcounts_all)
		overall_langcounts = sum_counter(langcounts_all)
		pprint(overall_htcounts.most_common(10))
		pprint(overall_langcounts.most_common(10))

	t2 = process_time() 

	print("Elapsed time:", t1, t2) 
   
	print("Elapsed time during the whole program in nanoseconds:", t1-t2)

def read_arguments(argv):
	# Initialise Variables
	inputfile = ''
	# search_type = 'hashtags'
	
	## Try to read in arguments
	try:
		opts, args = getopt.getopt(argv,"hi:tms:")
	except getopt.GetoptError as error:
		print(error)
		print_usage()
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print_usage()
			sys.exit()
		elif opt in ("-i"):
			inputfile = arg
		# elif opt in ("-m"):
		#    search_type = 'hashtags'
		# elif opt in ("-t"):
		#    search_type = 'language'
		
	# Return all the arguments
	return inputfile


if __name__ == '__main__':
	main(sys.argv[1:])

