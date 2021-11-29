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

def output_final(terms):
    """Reduce one group."""
    # iterate through each term
    # terms = [term for term in group]
    normalization_sums = defaultdict(int)
    for line in terms:
        idfk = line.split("\t")[-1].replace("\n", "")
        tf_ik = line.split("\t")[-2]
        doc_id = line.split("\t")[1]
        normalization_sums[doc_id] += pow(float(idfk) * float(tf_ik), 2)
    
    for value in normalization_sums:
        print("values " + value + ": " + str(normalization_sums[value]))
    dir = 'output'
    if not os.path.exists(dir):
        os.makedirs(dir)
    else:
        filelist = glob.glob(os.path.join(dir, "*"))
        for f in filelist:
            os.remove(f)
    with open('output/part00000', 'a') as a, open('output/part00001', 'a') as b, open("output/part00002", 'a') as c:
        for term in terms:
            word = term.split("\t")[0]
            doc_id = int(term.split("\t")[1])
            tf_ik = term.split("\t")[-2]
            idfk = term.split("\t")[-1].replace("\n", "")
            normalization = normalization_sums[str(doc_id)]
            # print("docid: " + str(doc_id) + " : " + str(normalization))
            if doc_id % 3 == 0:
                a.write(f"{word} {idfk} {doc_id} {tf_ik} {normalization}\n")
            elif doc_id % 3 == 1:
                b.write(f"{word} {idfk} {doc_id} {tf_ik} {normalization}\n")
            else:
                c.write(f"{word} {idfk} {doc_id} {tf_ik} {normalization}\n")

"""input: <term> <doc_id> <freq (tf_ik)> <idfk>"""
"""output: <term> <idfk> <doc_id> <tf_ik> <normalization> """

def main():
    """Divide sorted lines into groups that share a key."""
    # pipeline_input = sys.stdin
    # sys.stdin = open("/dev/tty")
    inputs = [line for line in sys.stdin]

    output_final(inputs)

    # for key, group in itertools.groupby(pipeline_input, keyfunc):
    #     reduce_one_group(key, group)

if __name__ == "__main__":
    main()