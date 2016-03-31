# This file cleans up the output of the wikiextractor.py by:
# - Adding spaces around punctuation
# - Replacing numbers with '#'
# - Adding newlines after each period
# - Removing meta-data
#
# NOTE: This code does NOT lowercase all words, because case may
# be important for tagging.
#
# Author: Peter Plantinga
# Date: March 2016

import sys
import glob
import re

if len(sys.argv) != 2:
    print("Usage: python3 cleanup.py input_directory")
    sys.exit(1)

# Regex for adding spaces around punctuation
addspace = re.compile("[()/;:,\"«»]")

# Regex for replacing numbers with #
numbers = re.compile("[0-9,]*[0-9]+(.[0-9]+)?")

# Regex for periods
periods = re.compile("(?<![A-Z])[.][ \n]?")

# For each file, output a clean version
for filename in glob.glob(sys.argv[1] + "/*/*"):
    with open(filename) as f:
        with open(filename + "_clean", 'w') as w:
            for line in f:

                # Skip tags
                if line[0:5] == "<doc ":
                    f.readline() # Skip title line
                    f.readline() # Skip blank line
                elif line != "</doc>\n" and line.strip() != "":
                    line = numbers.sub("#", line)
                    line = addspace.sub(r' \g<0> ', line)
                    line = periods.sub(" .\n", line)
                    line = line.replace("  ", " ")
                    w.write(line)
