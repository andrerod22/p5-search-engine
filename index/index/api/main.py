import flask
import pathlib
import index

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
    with open(page_path, mode='r') as s:
        input = s.readlines()
        for line in input:
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