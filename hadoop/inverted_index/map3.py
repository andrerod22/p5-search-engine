#!/usr/bin/env python3

"""Map 2."""
import sys
import pdb
import csv

for line in sys.stdin:
    doc_id = line.split("\t")[1]
    sys.stdout.write(doc_id + "\t" + line)