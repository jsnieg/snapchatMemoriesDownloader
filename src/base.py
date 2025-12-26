import os

import time

import requests

import re

import threading

from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
from functools import partial

from bs4 import BeautifulSoup, Tag

from typing import LiteralString

from dataclasses import dataclass

from threading import Thread

from . import main

@dataclass
class Config:
    port: int = 8000
    directory: str = '../mydata/'
    memories: LiteralString = f'http://localhost:{port}/html/memories_history.html'

def create_http_server(config: Config) -> HTTPServer:
    config = Config()
    print(f"[SERVER] Serving {config.directory} at http://localhost:{config.port}")
    handler = partial(SimpleHTTPRequestHandler, directory=config.directory)
    return HTTPServer(("localhost", config.port), handler)

def run_server() -> None:
    """
    runServer function with no args.\n
    Purpose of this function is to start a server on thread-1,
    whilst "serving" forever.
    """
    http_server = create_http_server()
    http_server.serve_forever()

def run_beautiful_soup() -> None:
    """
    Docstring for runBeautifulSoup
    """
    time.sleep(1.5)
    page = get_webpage_text(SNAPCHAT_HTML_MEMORIES)
    soup = BeautifulSoup(markup=page.text, features='html.parser')
    table = soup.find("tbody")
    a_tag = table.find_all_next('a')
    print(f'Found {len(a_tag)} images and videos!')
    for a in a_tag:
        _a = a.get('onclick')
        # print(_getRawLink(_a))
    print("Done")

class LinkExtractor():
    ...

class ThreadCreator():
    def server_thread(self, func) -> Thread:
        return threading.Thread(target="")

    def soup_thread(self, func) -> Thread:
        return threading.Thread(target="")

class SnapchatMemoriesDownloader():
    def __init__(self):
        self.threads = ThreadCreator()
        
    def run(self) -> None:
        self.threads.server_thread()
        self.threads.soup_thread()

def general_information() -> None:
    """Function printing general information about the script. 7 days left to download your data, etc."""
    last_modified: float = os.path.getmtime(...)

def get_raw_links(tag: Tag) -> str:
    match = re.search(r"'(https://[^']+)'", tag)
    return match.group(1) if match else None

def get_webpage_text(url: str) -> str:
    """Pass in url to get text of a page in string returned."""
    r = requests.get(url)
    return r.text

def download_memories() -> None:
    ...