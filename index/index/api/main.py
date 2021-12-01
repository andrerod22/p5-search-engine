import flask
import pathlib
import index
from collections import defaultdict
from collections import Counter
import re

stop_words = set()
page_rank = {}
inverted_index = {}

#function below is copied from spec. need more time to understand. 
@index.app.before_first_request
def startup():
    """Load inverted index, pagerank, and stopwords into memory."""
    index_dir = pathlib.Path(__file__).parent.parent
    read_stopwords(index_dir)
    read_pagerank(index_dir)
    read_inverted_index(index_dir)

def read_stopwords(index_dir):
    """Read stopwords."""
    page_path = pathlib.Path(index_dir/"stopwords.txt")
    with open(page_path, 'r') as input:
        lines = input.readlines()
        for line in lines:
            line = line.replace("\n", "")
            stop_words.add(line)

def read_pagerank(index_dir):
    page_path = pathlib.Path(index_dir/"pagerank.out")
    with open(page_path, mode="r") as r:
        lines = r.readlines()
        for line in lines:
            doc_id, rank_score = line.split(",")
            rank_score = rank_score.replace("\n", "")
            page_rank[doc_id] = rank_score

def read_inverted_index(index_dir):
    index_path = pathlib.Path(index_dir/"inverted_index"/index.app.config['INDEX_PATH'])
    with open(index_path, mode="r") as r:
        lines = r.readlines()
        for line in lines:
            line = line.replace("\n", "")
            line = line.split(" ")
            # Sets the term as the key, and
            # the other numbers in the list as value
            inverted_index[line[0]] = line[1:]

@index.app.route('/api/v1/', methods=["GET"])
def list_services():
    context = {
        "hits": "/api/v1/hits/",
        "url": "/api/v1/"
    }
    return flask.jsonify(**context)


@index.app.route('/api/v1/hits/', methods=["GET"])
def handle_query():
    query = flask.request.args.get('q')
    query = clean(query)
    
    # 1) Get documents that have every word in the cleaned query.
    matched_docs = {} # maps doc_id to [term freq, norm_factor] for a term.
    query_info = {} # used to map term (word) to idf
    # first pass is unique to populate matched_docs
    firstpass = True
    for word in query:
        # get doc_ids with the term (word). 
        doc_ids = {}
        if word in inverted_index:
            index_line = inverted_index[word]
            counter = 0
            id_fk = float(index_line[0])
            query_info[word] = id_fk
            curr_doc_id = ""
            doc_data = []
            for i in range(len(index_line[1:])):
                if counter % 3 == 0:
                    curr_doc_id = index_line[i]
                elif counter % 3 == 1:
                    doc_data.append(index_line[i])
                elif counter % 3 == 2:
                    doc_data.append(index_line[i])
                    doc_ids[curr_doc_id] = doc_data
                    doc_data.clear()
                counter+=1
        else:
            print("Error, word was not found in inverted index")
            break
        if firstpass:
            matched_docs = doc_ids
            firstpass = False
        else:
            # intersect the two dictionaries
            matched_docs = {x:matched_docs[x] for x in matched_docs 
                            if x in doc_ids}
    
    # 2) calculate relevance score for each doc
    # calculate the vector for the query. [term frequency in query * idf, ...]
    term_freq = Counter([word for word in query])
    query_vec = []
    for word in query:
        # tf * idf 
        val = term_freq[word] * query_info[word]
        query_vec.append(val)

    # 3) TODO calculate the vector for each document and calculate the score. 
    # refer to spec for calculations. 
    # https://eecs485staff.github.io/p5-search-engine/#appendix-a-tfidf-calculation-walkthrough

    doc_scores = defaultdict(float) # maps doc_id to its dot product (as of now). 
    counter = 0
    for word in query:
        idf = query_info[word]
        for doc in matched_docs:
            # doc is a doc_id
            tf = matched_docs[doc][0]
            pos = float(tf) * float(idf)
            doc_scores[doc] += query_vec[counter] * pos 
        counter += 1
            
            

    



        


    

    # order documents by doc_id
    # ideas: use sort(), custom comparator. 


    return {"status" : "ok"}

def clean(dirty):
    #This function was tricky for no reason. 
    dirty = re.sub(r"[^a-zA-Z0-9 ]+", "", dirty).casefold().split()
    clean = []
    counter = 0
    while(counter < len(dirty)):
        if dirty[counter] not in stop_words:
            clean.append(dirty[counter])
        counter+=1
    return clean