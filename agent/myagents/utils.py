import json
import os
import http.client, urllib.parse, json
import requests

subscriptionKey = "a7d5d8590dc84a23b05af0cf7b513dd9"

def search_pages(query: str):
    host = 'api.bing.microsoft.com'
    path = '/v7.0/custom/search'
    mkt = 'en-US'

    params = '?mkt=' + mkt + '&q=' + query + '&customconfig=1'
    headers = {'Ocp-Apim-Subscription-Key': subscriptionKey}

    conn = http.client.HTTPSConnection(host)
    conn.request("GET", path + params, None, headers)
    response = conn.getresponse()

    result = response.read()
    return json.loads(result)

def search_images(query: str):
    assert False, "not implemented"