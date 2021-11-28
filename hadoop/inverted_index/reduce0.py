#!/usr/bin/env python3
"""Reduce 0."""
import sys
from pathlib import Path

# grouping stage is done by sort on command line
count = 0
for word in sys.stdin:
    count += 1

# output single integer 
count = str(count)
sys.stdout.write(count + "\t \n")
cwd = Path.cwd()
output_folder = Path(cwd / 'output0/')

# Create output0 with parents
try:
    Path.mkdir(output_folder, parents=True)
except(FileExistsError):
    pass

# Write the file
with open(output_folder / 'part-00000', 'w') as out_file:
    out_file.write(count + "\n")
