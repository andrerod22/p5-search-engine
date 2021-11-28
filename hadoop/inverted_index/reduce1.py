#!/usr/bin/env python3
"""Reduce 1."""
import sys
import math

# Read the document count from Job 0: 
with open("total_document_count.txt", 'r') as count:
    doc_count = int(count.readline().split("\n")[0])

reducer = {}

# Read from pipeline
lines = sys.stdin
sys.stdin = open("/dev/tty")
for line in lines:
    try: reducer[line.split(" ")[0]] += 1
    except KeyError:
        reducer[line.split(" ")[0]] = 1
    
# Reducer Format
reducer_formatted = {}
keys = [key for key in reducer]
for k in keys:
    breakpoint()
    term = k.split("\t")[0]
    doc_id = k.split("\t")[1]
    try: reducer_formatted[term] = reducer_formatted[term] + '\t' + doc_id 
    except KeyError:
        reducer_formatted[term] = term + '\t' + 
    