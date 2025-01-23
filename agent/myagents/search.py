from ..agent import Agent
from ..context import Context
from ..context import LLMMessage
from ..client import DeepSeek
import json
import os
import http.client, urllib.parse, json
import requests


class SearchAgent(Agent):
    description = "Search the web for the task and summarize the top 3 web content which is relevant to the task."
    def __init__(self):
        super().__init__("search.j2")

    def run(self, task: str, msg: Context):

        results = search_pages(f"'{task}'")
        
        search_results = []
        for result in results["webPages"]["value"]:
            search_results.append({
                'title': result["name"],
                'url': result["url"],
                'snippet': result["snippet"]
            })
        

        formatted_results = "Results:\n\n"
        for i, result in enumerate(search_results, 1):
            formatted_results += f"{i}. {result['title']}\n"
            formatted_results += f"Link: {result['url']}\n" 
            formatted_results += f"Summary: {result['snippet']}\n\n"
        
        answer = DeepSeek().ask(f"""
        You have searched the web for the task: {task}.
        The web content is as follows:
        {formatted_results}

        Please summarize the content which is relevant to the task.
        Return the summary in markdown format.
        """)

        return answer
    

subscriptionKey = os.getenv('SUBSCRIPTION_KEY')

def search_pages(query: str):
    host = 'api.bing.microsoft.com'
    path = '/v7.0/custom/search'
    mkt = 'en-US'
    
    # URL 编码查询参数
    encoded_query = urllib.parse.quote(query)
    params = f'?mkt={mkt}&q={encoded_query}&customconfig=1'
    
    headers = {'Ocp-Apim-Subscription-Key': subscriptionKey}

    conn = http.client.HTTPSConnection(host)
    conn.request("GET", path + params, None, headers)
    response = conn.getresponse()

    result = response.read()
    return json.loads(result)