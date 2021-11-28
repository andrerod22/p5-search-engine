#!/usr/bin/env python3
"""Map 0."""
import csv
import sys

# Pro-tip: Use the Python csv library and add the line csv.field_size_limit(sys.maxsize) 
# (doc_body is very large for some documents).
csv.field_size_limit(sys.maxsize)

# read from stdin and write the file to stdout:
for doc in csv.reader(sys.stdin):
    sys.stdout.write("document\t1\n")
