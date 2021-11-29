#!/usr/bin/env python3
"""Reduce 1."""
import sys
import itertools
import math
import csv
import os, glob
from collections import defaultdict

# Read the document count from Job 0: 
total_docs = 0
with open("total_document_count.txt", 'r') as count:
    total_docs = int(count.readline().split("\n")[0])

def reduce_one_group(key, group):
    """Reduce one group."""
    # iterate through each term
    # terms = [term for term in group]
    normalization_sums = defaultdict(int)
    terms = list(group)
    for line in terms:
        idfk = line.split("\t")[-1].replace("\n", "")
        tf_ik = line.split("\t")[-2]
        doc_id = line.split("\t")[0]
        normalization_sums[doc_id] += pow(float(idfk) * float(tf_ik), 2)
    # breakpoint()
    for term in terms:
        word = term.split("\t")[1]
        doc_id = int(term.split("\t")[2])
        tf_ik = term.split("\t")[-2]
        idfk = term.split("\t")[-1].replace("\n", "")
        normalization = normalization_sums[str(doc_id)]
        sys.stdout.write(f"{word}\t{idfk}\t{doc_id}\t{tf_ik}\t{normalization}\n")

"""input: <term> <doc_id> <freq (tf_ik)> <idfk>"""
"""output: <term> <idfk> <doc_id> <tf_ik> <normalization> """

def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]

def main():
    """Divide sorted lines into groups that share a key."""
    pipeline_input = sys.stdin
    sys.stdin = open("/dev/tty")
    for key, group in itertools.groupby(pipeline_input, keyfunc):
        reduce_one_group(key, group)

    # for key, group in itertools.groupby(pipeline_input, keyfunc):
    #     reduce_one_group(key, group)

if __name__ == "__main__":
    main()