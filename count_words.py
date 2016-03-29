# This file takes one parameter -- a directory and outputs three things:
# - Top ten words by frequency
# - Number of words tokens
# - Number of word types
#
# We assume the input directory is the same format as that output by
# WikiExtractor.py
#
# Author: Peter Plantinga
# Date: March 2016

import sys
import glob
import collections
import operator

# Check input parameters
if len(sys.argv) != 2:
    print("Usage: python3 count_words.py input_directory")
    sys.exit(1)

word_counts = collections.defaultdict(int)
total_words = 0

# For each file in the directory
for filename in glob.glob(sys.argv[1] + "/*/*"):
    with open(filename) as f:
        for line in f:
            
            # Ignore empty lines and lines that are just metadata
            if line != "" and line[0] != "<":
                line = line.split()

                # Increment count of each word and total words
                for word in line:
                    word_counts[word] += 1
                    total_words += 1

# Sort list to find top 10
sorted_counts = sorted(word_counts.items(), key=operator.itemgetter(1), reverse=True)

# Output relevant information
print("Top 10 words: ")
for i in range(10):
    print("\t" + str(sorted_counts[i]))
print("Word tokens: " + str(total_words))
print("Word types: " + str(len(word_counts)))

