"""Main for api."""
import flask
import pathlib
import index
from collections import defaultdict
from collections import Counter
import math
import operator
import re

stop_words = set()
page_rank = {}
inverted_index = {}

# function below is copied from spec. need more time to understand.


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
    """Read page ranks and store."""
    page_path = pathlib.Path(index_dir/"pagerank.out")
    with open(page_path, mode="r") as r:
        lines = r.readlines()
        for line in lines:
            doc_id, rank_score = line.split(",")
            rank_score = rank_score.replace("\n", "")
            page_rank[doc_id] = rank_score


def read_inverted_index(index_dir):
    """Read inverted index."""
    tmp = pathlib.Path(index_dir/"inverted_index")
    index_path = pathlib.Path(tmp/index.app.config['INDEX_PATH'])
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
    """List services."""
    context = {
        "hits": "/api/v1/hits/",
        "url": "/api/v1/"
    }
    return flask.jsonify(**context)


@index.app.route('/api/v1/hits/', methods=["GET"])
def handle_query():
    """Handle query."""
    query = flask.request.args.get('q')
    query = clean(query)
    # 1) Get documents that have every word in the cleaned query.

    # maps doc_id to [term freq, norm_factor, ...] for a term.
    matched_docs = {}
    # used to map term (word) to idf
    query_info = {}
    for word in query:
        # get doc_ids with the term (word).
        # breakpoint()
        if word in inverted_index:
            index_line = inverted_index[word]
            counter = 0
            id_fk = float(index_line[0])
            query_info[word] = id_fk
            curr_doc_id = ""
            doc_data = []
            sliced = index_line[1:]
            for i in range(len(sliced)):
                if counter % 3 == 0:
                    curr_doc_id = sliced[i]
                elif counter % 3 == 1:
                    doc_data.append(sliced[i])
                elif counter % 3 == 2:
                    doc_data.append(sliced[i])
                    if curr_doc_id in matched_docs:
                        matched_docs[curr_doc_id].extend([x for x in doc_data])
                    else:
                        matched_docs[curr_doc_id] = [x for x in doc_data]
                    doc_data.clear()
                counter += 1
        else:
            print("Error, word was not found in inverted index")
            return {"hits": []}

    # Eliminate documents that don't have all the terms.
    matched_docs = {x: matched_docs[x] for x in matched_docs
                    if len(matched_docs[x]) == len(query) * 2}

    # breakpoint()
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

    # maps doc_id to its dot product (as of now).
    doc_scores = defaultdict(float)
    counter = 0

    # breakpoint()
    for doc in matched_docs:
        vals = matched_docs[doc]  # [tf, norm, tf, norm ...]
        query_ind = 0
        for i in range(len(vals)):
            if i % 2 == 0:
                tf = vals[i]
                idf = query_info[query[query_ind]]
                pos = float(tf) * float(idf)
                doc_scores[doc] += query_vec[query_ind] * pos
            if i % 2 == 1:
                # gets normalization
                query_ind += 1

    # Integrate pageRank

    weight = 0.5
    try:
        weight = flask.request.args['w']
    except KeyError:
        pass

    for doc in doc_scores:
        # doc_p = tfIdf
        # if doc == 214936:
        #     breakpoint()
        dot_p = doc_scores[doc]
        norm_total = 0
        for num in query_vec:
            norm_total += pow(float(num), 2)
        norm_q = math.sqrt(norm_total)
        norm_d = math.sqrt(float(matched_docs[doc][1]))
        tf_idf = dot_p / (norm_q * norm_d)

        score = (float(page_rank[str(doc)]) * float(weight)
                 + tf_idf * (1 - float(weight)))

        doc_scores[doc] = score

    # order documents by scores then by doc_id

    doc_list = [{"docid": int(x), "score": doc_scores[x]} for x in doc_scores]

    # Stable complex sort, secondary attribute first.
    doc_list = sorted(doc_list, key=operator.itemgetter('docid'))
    doc_list = sorted(doc_list, key=operator.itemgetter('score'), reverse=True)

    # docid
    # score
    context = {
        "hits": [x for x in doc_list]
    }
    return flask.jsonify(**context)


def clean(dirty):
    """Clean query."""
    # This function was tricky for no reason.
    dirty = re.sub(r"[^a-zA-Z0-9 ]+", "", dirty).casefold().split()
    clean = []
    counter = 0
    while(counter < len(dirty)):
        if dirty[counter] not in stop_words:
            clean.append(dirty[counter])
        counter += 1
    return clean
