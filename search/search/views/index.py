import heapq
import queue
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

    params = {'q': query, 'w': weight}
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
    # Done modifying variables, such that we can then do heapqmerge on all results. 

    first_result = result_queue.get()
    second_result = result_queue.get()
    third_result = result_queue.get()
    
    first_arr = [f"{x['docid']} {x['score']}" for x in first_result['hits']]
    second_arr = [f"{x['docid']} {x['score']}" for x in second_result['hits']]
    third_arr = [f"{x['docid']} {x['score']}" for x in third_result['hits']]

    result = []
    count = 0
    for line in merge(first_arr, second_arr, third_arr):
        if count == 10:
            break
        result.append(line) 
        count +=1
    
    for res in result:
        print(res)

    context = {}
    return flask.render_template("index.html", **context)


def server_call(api_url, params, result_queue):
    """"""
    response = requests.get(api_url, params=params)
    response_json = response.json()
    result_queue.put(response_json)
