#!/usr/bin/env python3
"""Map 1."""
import csv
import sys
import re
import pdb

csv.field_size_limit(sys.maxsize)
with open("stopwords.txt", 'r') as input:
    stop_words = set(input.readlines())

# Uncommment sys.stdin = open line if you want to debug map/reduce
pipeline_input = csv.reader(sys.stdin)
#sys.stdin = open("/dev/tty")
for line in pipeline_input:
    # Initilize each part of the document
    doc_id = line[0]
    doc_title = str(line[1].split())
    doc_body = str(line[2].split())
    # Remove non-alphanumeric characters (that also aren’t spaces)
    doc_title = re.sub(r"[^a-zA-Z0-9]+", " ", doc_title).casefold().split()
    doc_body = re.sub(r"[^a-zA-Z0-9]+", " ", doc_body).casefold().split()
    terms = doc_title + doc_body
    for term in terms:
        if term+"\n" not in stop_words:
            # Note: We add the doc_id to the system write to allow us
            # to distinguish between duplicate words
            # Example: 'art' in doc_id 1 and 'art' in doc_id 2 are treated as
            # unique keys in reduce1.py
            sys.stdout.write(term + "\t" + doc_id + "\t" + "1\n")
            # sys.stdout.write(term + "\t" + "1\n")

"""<term> <doc_id> <1>"""