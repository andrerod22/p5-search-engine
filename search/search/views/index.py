import flask 
import search
import requests
from heapq import merge
from threading import Thread
from queue import Queue



@search.app.route('/', methods=["GET"])
def render_index():
    """Renders index."""

    query = flask.request.args.get('q')
    weight = flask.request.args.get("w")

    if query is None and weight is None:
        return flask.render_template("index.html")

    params = flask.request.args
    # Access the urls for the apis through 
    api_urls = search.app.config['SEARCH_INDEX_SEGMENT_API_URLS']

    result_queue = Queue(maxsize=3)
    server_1_thread = Thread(target=server_call, args=(api_urls[0], params, result_queue))
    server_2_thread = Thread(target=server_call, args=(api_urls[1], params, result_queue))
    server_3_thread = Thread(target=server_call, args=(api_urls[2], params, result_queue))
    
    server_1_thread.start()
    server_2_thread.start()
    server_3_thread.start()
    server_1_thread.join()
    server_2_thread.join()
    server_3_thread.join()
    # Once queue is full, pop the queue for json results from index server. 
    first_result = result_queue.get()
    second_result = result_queue.get()
    third_result = result_queue.get()
    iter_list = [first_result['hits'], second_result['hits'], third_result['hits']]

    result = []
    count = 0
    for line in merge(*iter_list, key=lambda r : (r['score'], -r['docid'])):
        if count == 10:
            break
        result.append(line)
        count+= 1

    connection = search.model.get_db()
    
    res_array = [] # a list of dict objects
    for res in result:
        doc_id = res['docid']
        # sql = f""""SELECT title, url, summary FROM documents WHERE docid={doc_id}"""
        cur = connection.execute(
                "SELECT title, url, summary FROM documents WHERE docid=%s" % doc_id)
        res_array.append(cur.fetchone())
        # print(cur.fetchall())

    context = {"result": res_array}
    return flask.render_template("index.html", **context)


def server_call(api_url, params, result_queue):
    """Make a API call to an index server"""
    response = requests.get(api_url, params=params)
    response_json = response.json()
    result_queue.put(response_json)
