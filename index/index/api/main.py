import flask
import pathlib
import index

#function below is copied from spec. need more time to understand. 
@index.app.before_first_request
def startup():
    """Load inverted index, pagerank, and stopwords into memory."""
    index_dir = pathlib.Path(__file__).parent.parent
    # read_stopwords(index_dir)
    # read_pagerank(index_dir)
    # read_inverted_index(index_dir)