import os

import time

import requests

import re

from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
from functools import partial

from bs4 import BeautifulSoup, Tag

from typing import LiteralString

# c-like structs
from dataclasses import dataclass

from . import main

# Config
# TODO: this needs to be in venv upon when feeding information via command line
PORT = 8000
SNAPCHAT_HTML_DIR: str | None = '../mydata/'
SNAPCHAT_HTML_MEMORIES: LiteralString = f'http://localhost:{PORT}/html/memories_history.html'

@dataclass
class Config:
    port: int = 8000
    snapchat_html_directory: str = '../mydata/'
    snapchat_html_memories: LiteralString = f'http://localhost:{PORT}/html/memories_history.html'

class SnapchatMemoriesDownloader():
    ...

def get_raw_links(tag: Tag) -> str:
    match = re.search(r"'(https://[^']+)'", tag)
    return match.group(1) if match else None

def get_webpage_text(url: Config) -> requests.Response:
    return requests.get(url)

def download_memories() -> None:
    ...

def create_http_server(config: Config) -> HTTPServer:
    config = Config()
    print(f"[SERVER] Serving {config.snapchat_html_directory} at http://localhost:{config.port}")
    handler = partial(SimpleHTTPRequestHandler, directory=config.snapchat_html_directory)
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