"""Flask serverside for rendering search engine results."""
from operator import itemgetter
from heapq import merge
from threading import Thread
from queue import Queue
import flask
import requests
import search


@search.app.route('/', methods=["GET"])
def render_index():
    """Render index."""
    # query = flask.request.args.get('q')
    # weight = flask.request.args.get('w')
    # print(f"WEIGHT: {weight}")

    if flask.request.args.get('q') is None:
        context = {
           "result": [],
           "query": "",
           "weight": "",
           "queried": False
           }
        return flask.render_template("index.html", **context)

    # params = flask.request.args
    params = {"q": flask.request.args.get('q'),
              "w": flask.request.args.get('w')}
    # Access the urls for the apis through
    api_urls = search.app.config['SEARCH_INDEX_SEGMENT_API_URLS']

    result_queue = Queue(maxsize=3)
    server_1_thread = Thread(target=server_call,
                             args=(api_urls[0], params, result_queue))
    server_2_thread = Thread(target=server_call,
                             args=(api_urls[1], params, result_queue))
    server_3_thread = Thread(target=server_call,
                             args=(api_urls[2], params, result_queue))

    server_1_thread.start()
    server_2_thread.start()
    server_3_thread.start()
    server_1_thread.join()
    server_2_thread.join()
    server_3_thread.join()
    # Once queue is full, pop the queue for json results from index server.
    # first_res = result_queue.get()['hits']
    # sec_res = result_queue.get()['hits']
    # third_res = result_queue.get()['hits']
    # iter_list = [
    #     first_result['hits'],
    #     second_result['hits'],
    #     third_result['hits']
    # ]

    result = []
    count = 0
    for line in merge(result_queue.get()['hits'],
                      result_queue.get()['hits'],
                      result_queue.get()['hits'],
                      key=itemgetter('score'),
                      reverse=True):
        if count == 10:
            break
        result.append(line)
        count += 1

    # connection = search.model.get_db()

    res_array = []  # a list of dict objects
    for res in result:
        # doc_id = res['docid']
        cur = search.model.get_db().execute(
                f"""SELECT title, url, summary
                FROM documents WHERE docid={res['docid']}""")
        # db_obj = cur.fetchone()
        res_array.append(cur.fetchone())

    # breakpoint()

    context = {
        "result": res_array,
        "query": flask.request.args.get('q'),
        "weight": flask.request.args.get('w'),
        "queried": True
        }
    return flask.render_template("index.html", **context)


def server_call(api_url, params, result_queue):
    """Make a API call to an index server."""
    response = requests.get(api_url, params=params)
    response_json = response.json()
    result_queue.put(response_json)
