import os
import platform

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

config = Config()

def create_http_server() -> HTTPServer:
    """Create HTTP server at a given port by the config dataclass (struct)."""
    print(f"[SERVER] Serving {config.directory} at http://localhost:{config.port}")
    try:
        handler = partial(SimpleHTTPRequestHandler, directory=config.directory)
        return HTTPServer(("localhost", config.port), handler)
    except:
        raise "Server could not be created."

def general_information() -> None:
    """Function printing general information about the script. 7 days left to download your data, etc."""
    print('')
    if platform.system() == 'Windows':
        last_modified: float = os.path.getmtime(...)

def get_raw_links(tag: Tag) -> str:
    """Get raw download links when a Tag from BS4 is passed through. This will let _download_memories(parameter)_ download all wanted files."""
    if tag is None:
        return None
    match = re.search(r"'(https://[^']+)'", tag)
    return match.group(1) if match else None

def get_webpage_text(url: str) -> str:
    """Pass in url to get text of a page in string returned."""
    r = requests.get(url)
    return r.text

def run_server() -> None:
    """Create and run server forever in Thread-1."""
    http_server = create_http_server()
    http_server.serve_forever()

def run_beautiful_soup() -> None:
    """The brains behind this script. Runs BS4, looping through raw HTML finding all tags required to find download links. Creates new Thread instance working separately."""
    time.sleep(1.5)
    page: str = get_webpage_text(config.memories)
    soup = BeautifulSoup(markup=page, features='html.parser')
    table = soup.find("tbody")
    a_tags = table.find_all_next('a')
    print(f'Found {len(a_tags)} images and videos!')
    for tags in a_tags:
        tag = tags.get('onclick')
        print(get_raw_links(tag))
    print("Done")

class LinkExtractor():
    ...

# class ThreadCreator():
#     def server_thread(self, func) -> Thread:
#         return threading.Thread(target="")

#     def soup_thread(self, func) -> Thread:
#         return threading.Thread(target="")

class SnapchatMemoriesDownloader():
    def __init__(self):
        # self.threads = ThreadCreator()
        ...
        
    def run(self) -> None:
        # self.threads.server_thread()
        # self.threads.soup_thread()
        ...

def download_memories() -> None:
    ...