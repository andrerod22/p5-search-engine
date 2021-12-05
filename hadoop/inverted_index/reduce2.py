#!/usr/bin/env python3
"""Reduce 1."""
import sys
import itertools


# Read the document count from Job 0: 

def reduce_one_group(key, group):
    """Reduce one group."""
    #for each document sum up the all its (tfiks * idfks)
    prev_doc_id = None
    words = list(group)
    if len(words) == 1:
        doc_id = words[0].split('\t')[1]
        idfk = words[0].split('\t')[3]
        sys.stdout.write(f"{key}\t{doc_id}\t{1}\t{idfk}") 
    else:
        # we don't want to lose tf_ik
        prev_doc_id = words[0].split("\t")[1]
        tf_ik = 1 # for the first iteration
        for word in words[1:]:
            doc_id = word.split("\t")[1]
            if doc_id != prev_doc_id:
                idfk = word.split("\t")[3]
                # normalization_sums[doc_id] += pow(idfk * tf_ik, 2)
                sys.stdout.write(f"{key}\t{prev_doc_id}\t{tf_ik}\t{idfk}")
                prev_doc_id = doc_id
                tf_ik = 1
            else:
                tf_ik += 1
        doc_id = words[-1].split("\t")[1]
        idfk = word.split("\t")[3]
        sys.stdout.write(f"{key}\t{doc_id}\t{tf_ik}\t{idfk}")
    

"""input: <term> <doc_id> <1> <idfk>"""
# do we ever use the 1 ? --^
"""write based doc_id, doc_id % 3 """
"""output: <term> <doc_id> <freq (tf_ik)> <idfk>"""

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
Job 1
Map1.py --> Reduce1.py --> Calculate TFik, 
<TERM> \t <DOC_ID> \t <TERM FREQUENCY>
document        1   1
document        1   1
mike    1 1
bostock 1 1
made    1 1
d3      1 1
js      1 1
cool    1 1
document        2 1
flaw    2 1
human   2 1
character       2 1
build   2 1
maintenance     2 1
kurt    2 1
vonnegut        2 1
document        3 1
originality     3 1
fine    3 1
art     3 1
remembering     3 1
hear    3 1
forgetting      3 1
heard   3 1
laurence        3 1
peter   3 1

"""



""" 
reducer = {}
reducer_formatted = {}
keys = [key for key in reducer]
for k in keys:
    breakpoint()
    term = k.split("\t")[0]
    doc_id = k.split("\t")[1]

    try: reducer_formatted[term] = reducer_formatted[term] + '\t' + doc_id 
    except KeyError:
        reducer_formatted[term] = term + '\t' + doc_id

# for term in reducer_formatted:
"""




# TFIK old
"""
#if len(words) == 1:
        #print(f"{key}\t{doc_id}\t{1}") 
    
    # if key == 'document':
        #breakpoint()
    
    for word in words:
        # breakpoint()
        # print(list(group))
        doc_id = word.split("\t")[1]
        if doc_id != prev_doc_id:
            if prev_doc_id != None:
                print(f"{key}\t{doc_id}\t{tfik}")
            tfik = 1
            # doc_count += 1 # continue?
            prev_doc_id = doc_id
        else:
            tfik += 1
        word_count += 1
        # count = line.split("\t")[2].replace("\n","")
        # word_count += int(count)
    if word_count == 1:
       print(f"{key}\t{doc_id}\t{tfik}") 
    # Calculate idfk
    # idfk = math.log(total_docs / doc_count)
"""