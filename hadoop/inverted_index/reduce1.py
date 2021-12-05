#!/usr/bin/env python3
"""Reduce 1."""
import sys
import itertools
import math
import csv
from itertools import tee

# Read the document count from Job 0: 
total_docs = 0
with open("total_document_count.txt", 'r') as count:
    total_docs = int(count.readline().split("\n")[0])

def reduce_one_group(key, group):
    """Reduce one group."""
    # Possible Optimation: use less memory 
    doc_count = 0 #n_k
    prev_doc_id = None
    length = 0
    doc_ids = []
    # group_iter = tee(group)
    for line in group:
        # if the doc_id is different then we want to increment n_k
        doc_id = line.split("\t")[1]
        doc_ids.append(doc_id)
        if doc_id != prev_doc_id:
            doc_count += 1
            prev_doc_id = doc_id
        length += 1
        
    # Calculate idfk
    # breakpoint()
    idfk = math.log10(total_docs / doc_count)
    for id in doc_ids:
        sys.stdout.write(f"{key}\t{id}\t{1}\t{idfk}\n")

def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]

def main():
    """Divide sorted lines into groups that share a key."""
    pipeline_input = sys.stdin
    for key, group in itertools.groupby(pipeline_input, keyfunc):
        reduce_one_group(key, group)

if __name__ == "__main__":
    main()



"""
<TERM> <DOC_ID> <TFIK>
art     3       1
bostock 1       1
build   2       1
character       2       1
cool    1       1
d3      1       1
document        1       2
document        2       1
document        3       1
fine    3       1
flaw    2       1
forgetting      3       1
hear    3       1
heard   3       1
human   2       1
js      1       1
kurt    2       1
laurence        3       1
made    1       1
maintenance     2       1
mike    1       1
originality     3       1
peter   3       1
remembering     3       1
vonnegut        2       1


"""