#!/usr/bin/env python3
"""Final reducer"""
import sys
import itertools


def reduce_one_group(key, group):
    """Reduce one group."""
    for line in group:
        normalization = line.split("\t")[-1].replace("\n", "")
        tf_ik = line.split("\t")[-2]
        doc_id = line.split("\t")[-3]
        idfk = line.split("\t")[-4]
        word = line.split("\t")[-5]
        sys.stdout.write(f"{word} {idfk} {doc_id} {tf_ik} {normalization}\n")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()