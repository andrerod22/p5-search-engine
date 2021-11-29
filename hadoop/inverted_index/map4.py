#!/usr/bin/env python3

"""Map 2."""
import sys
import pdb
import csv

for line in sys.stdin:
    doc_id = line.split("\t")[2]
    last_job_map_key = int(doc_id) % 3
    sys.stdout.write(str(last_job_map_key) + '\t' + line)