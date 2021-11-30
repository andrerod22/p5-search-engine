#!/usr/bin/env python3
"""Final reducer"""
import sys
import itertools


def reduce_one_group(key, group):
    """Reduce one group."""
    # one group should be one key. ex: doc_id % 3 = 0.
    # if doc_id % 3 = 0, then all should map to part-0
    
    term_dic = {}
    terms = list(group)
    for line in terms:
        normalization = line.split("\t")[-1].replace("\n", "")
        tf_ik = line.split("\t")[-2]
        doc_id = line.split("\t")[-3]
        idfk = line.split("\t")[-4]
        word = line.split("\t")[-5]
        term_info = [doc_id, tf_ik, normalization]
        if word in term_dic:
            term_dic[word].extend(term_info)
        else:
            #the first time we see a word. 
            term_info.insert(0, idfk)
            term_dic[word] = term_info
        # sys.stdout.write(f"{word} {idfk} {doc_id} {tf_ik} {normalization}\n")
    for term in terms:
        word = term.split("\t")[-5]
        if word in term_dic:
            sys.stdout.write(f"{word} ")
            for i, num in enumerate(term_dic[word]):
                sys.stdout.write(f"{num}")
                if i != len(term_dic[word]) - 1:
                    sys.stdout.write(" ")
            sys.stdout.write("\n")
            term_dic.pop(word)


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()