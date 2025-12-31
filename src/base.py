import os
import platform

import time

import requests

import re

from http.server import HTTPServer, SimpleHTTPRequestHandler
from functools import partial

from bs4 import BeautifulSoup, Tag

from dataclasses import dataclass

from urllib.request import urlretrieve

from datetime import datetime, timedelta

from statx import statx

from requests import Request, Response

@dataclass
class Config:
    port: int = 8000
    directory: str = '../mydata'
    memories: str = f'http://localhost:{port}/html/memories_history.html'


config = Config()
urls: list[str] = []


def create_http_server(config: Config) -> HTTPServer:
    """Create HTTP server at a given port by the config dataclass (struct)."""
    print(f"[SERVER] Serving {config.directory} at http://localhost:{config.port}")
    try:
        handler = partial(SimpleHTTPRequestHandler, directory=config.directory)
        return HTTPServer(("localhost", config.port), handler)
    except:
        raise "Server could not be created."


def dir_modified_date(config: Config) -> timedelta:
    """Get date of last modified/created date of a directory based on platform's OS and return timedelta."""
    directory_date = None
    if platform.system() == 'Windows':
        directory_date = os.path.getmtime(config.directory)
    else:
        stat = os.stat(config.directory)
        try:
            directory_date = datetime.fromtimestamp(stat.st_birthtime)
        except AttributeError as exception:
            btime = statx(config.directory).btime
            if btime: 
                directory_date = datetime.fromtimestamp(btime)
    now = datetime.now()
    return now - directory_date


def check_directory(config: Config) -> None:
    """Function to check if directory is not older than 7 days and whether it does exist."""
    directory_date = None
    now = datetime.now()

    if os.path.isdir(config.directory):
        assert True
    else:
        assert False, f"{config.directory} has not been found, make sure you've requested your data from Snapchat."

    if platform.system() == 'Windows':
        directory_date = os.path.getmtime(config.directory)
    else:
        stat = os.stat(config.directory)
        try:
            directory_date = datetime.fromtimestamp(stat.st_birthtime)
        except AttributeError as exception:
            btime = statx(config.directory).btime
            if btime: 
                directory_date = datetime.fromtimestamp(btime)
    
    d = now - directory_date

    if d.days >= 7:
        assert False, f'{config.directory} is older than 7 days, meaning your data is no longer available to download. Please request new data from Snapchat.'
    else:
        assert True, f'{config.directory} is not older than 7 days.'


def get_raw_links(tag: Tag) -> str:
    """Get raw download links when a Tag from BS4 is passed through. This will let _download_memories(parameter)_ download all wanted files."""
    if tag is None:
        return None
    match = re.search(r"'(https://[^']+)'", tag)
    return match.group(1) if match else None


def get_webpage_response(url: str, once: bool) -> Response:
    """Pass in url to get response from the page in string returned."""
    res = requests.get(url)
    # Needed or not? Downloading and saving will take long enough before rate limiter kicks in.
    # delay: int | float = 0 if once == True else 0.75
    # time.sleep(delay)
    if res.status_code != 200:
        print(f"Status code: {res.status_code}\n")
        print(res.headers)
    else:
        return res


def run_server(config: Config) -> None:
    """Create and run server forever in Thread-1."""
    http_server = create_http_server(config)
    http_server.serve_forever()


def run_beautiful_soup(config: Config) -> None:
    """The brains behind this script. Runs BS4, looping through raw HTML finding all tags required to find download links. Creates new Thread instance working separately."""
    time.sleep(1.5)
    page: str = get_webpage_response(config.memories, True)
    soup = BeautifulSoup(markup=page.text, features='html.parser')
    table = soup.find("tbody")
    a_tags = table.find_all_next('a')
    print(f'Found {len(a_tags)} images and videos!')
    for tags in a_tags:
        tag = tags.get('onclick')
        urls.append(get_raw_links(tag))
    for url in urls:
        download(url)
    # download(urls)
    # download(urls[0])


def download(url: str) -> None:
    """Download files from the URL provided and save it to respective file type and name."""
    res: Response = get_webpage_response(url, False)
    file_type: str = res.headers['Content-Type']
    content_name: str = res.headers['Content-Disposition']
    file_name: str = content_name.split(";")[1].split('=')[1].strip('"') # I could've used regex here, but I already did so enjoy this.


def move_files() -> None:
    """Function to move files downloaded from one directory to another directory of user's choosing."""
    ...