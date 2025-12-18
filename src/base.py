import os

import time

import requests

import re

from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
from functools import partial

from bs4 import BeautifulSoup

from typing import LiteralString

from . import main

# Config
# TODO: this needs to be in venv upon when feeding information via command line
PORT = 8000
SNAPCHAT_HTML_DIR: str | None = '../mydata/'
SNAPCHAT_HTML_MEMORIES: LiteralString = f'http://localhost:{PORT}/html/memories_history.html'

class SnapchatMemoriesDownloader():
    pass

def _getRawLink(func) -> None:
    match = re.search(r"'(https://[^']+)'", func)
    return match.group(1) if match else None

def getWebPageText(url: str = SNAPCHAT_HTML_MEMORIES) -> requests.Response:
    """
    getWebPageText is designed to return HTML data for BeautifulSoup4 to scrape through.
    
    :param url: Web page URL string to get HTML data from.
    :type url: str
    :return: Returns a text string of raw HTML data from the get requested web path.
    :rtype: Response
    """
    print(f"[REQUEST] Requesting a raw HTML string from {url}")
    return requests.get(url)

def downloadMemories() -> None:
    pass

def runServer() -> None:
    """
    runServer function with no args.\n
    Purpose of this function is to start a server on thread-1,
    whilst "serving" forever.
    """
    handler: partial[SimpleHTTPRequestHandler] = partial(SimpleHTTPRequestHandler, directory=SNAPCHAT_HTML_DIR)
    http_server: HTTPServer = HTTPServer(("localhost", PORT), handler)
    print(f"[SERVER] Serving {SNAPCHAT_HTML_DIR} at http://localhost:{PORT}")
    http_server.serve_forever()

def runBeautifulSoup() -> None:
    """
    Docstring for runBeautifulSoup
    """
    time.sleep(1.5)
    page = getWebPageText(SNAPCHAT_HTML_MEMORIES)
    soup = BeautifulSoup(markup=page.text, features='html.parser')
    table = soup.find("tbody")
    a_tag = table.find_all_next('a')
    print(f'Found {len(a_tag)} images and videos!')
    for a in a_tag:
        _a = a.get('onclick')
        # print(_getRawLink(_a))
    print("Done")