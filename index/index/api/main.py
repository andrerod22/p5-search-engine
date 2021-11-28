import re
import flask
import index
import math
from pathlib import Path

with open("stopwords.txt", 'r') as input:
    stop_words = set(input.readlines())

@index.app.route('/api/v1/', methods=['GET'])
def list_services():
    context = {
        "hits": "/api/v1/hits/",
        "url": "/api/v1/"
    }
    return flask.jsonify(**context)

@index.app.route('/api/v1/hits/', methods=['GET'])
def list_hits():
    # Get query parameter and format: 
    query = flask.request.args.get('q')
    query = re.sub(r'[^a-zA-Z0-9 ]+', ' ', query)
    query_list = query.split(' ')
    for term in query_list:
        if term in stop_words:
            query_list.remove(term)
    
    # Get weight query parameter:
    if flask.request.args.get('w'):
        weight = flask.request.args.get('w') 
    else:
        weight = 0.5

    query_dict = {}
    for item in query_list:
        if item in query_dict:
            query_dict[item] += 1
        else:
            query_dict[item] = 1
    print(query_list)



