import os
import shutil
import platform

import time

import requests

import re

from http.server import HTTPServer, SimpleHTTPRequestHandler
from functools import partial

from bs4 import BeautifulSoup, Tag

from dataclasses import dataclass

from datetime import datetime, timedelta

from statx import statx

from requests import Request, Response

# from tqdm import tqdm

@dataclass
class Config:
    port: int = 8000
    directory: str = '../mydata'
    memories: str = f'http://localhost:{port}/html/memories_history.html'
    source_dir: str = '../files'
    target_dir: str = '?'


class quietServer(SimpleHTTPRequestHandler):
    """Classs inherting to silence the HTTP server's logs."""
    def log_message(self, format, *args):
        pass


config = Config()
urls: list[str] = []
total_length: int = 0


def create_http_server(config: Config) -> HTTPServer:
    """Create HTTP server at a given port by the config dataclass (struct)."""
    print(f"[SERVER] Serving {config.directory} at http://localhost:{config.port}")
    try:
        handler = partial(quietServer, directory=config.directory)
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
    now: datetime = datetime.now()
    return now - directory_date


def check_directory(config: Config) -> None:
    """Function to check if directory is not older than 7 days and whether it does exist."""
    directory_date = dir_modified_date(config)

    if os.path.isdir(config.directory):
        assert True
    else:
        assert False, f"{config.directory} has not been found, make sure you've requested your data from Snapchat and that it is inside your designated directory."

    if directory_date.days >= 7:
        assert False, f'{config.directory} is older than 7 days, meaning your data is no longer available to download. Please request new data from Snapchat.'
    else:
        assert True, f'{config.directory} is not older than 7 days.'


def get_raw_links(tag: Tag) -> str:
    """Get raw download links when a Tag from BS4 is passed through. This will let _download_memories(parameter)_ download all wanted files."""
    if tag is None:
        return None
    match = re.search(r"'(https://[^']+)'", tag)
    return match.group(1) if match else None


def get_webpage_response(url: str, once: bool, stream: bool = False) -> Response:
    """Pass in url to get response from the page in string returned."""
    res = requests.get(url, stream=stream)
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
    # for url in urls:
    #     download(config, url)
    download(config, urls[0])


def download(config: Config, url: str) -> None:
    """Download files from the URL provided and save it to respective file type and name."""
    if url == "" or url is None: assert False, "Empty url was fed to the download function."
    res: Response = get_webpage_response(url, False, True)
    content_name: str = res.headers['Content-Disposition']
    current_length: int = int(res.headers['Content-Length'])
    # total_length += current_length
    file_name: str = content_name.split(";")[1].split('=')[1].strip('"') # I could've used regex here, but I already did so enjoy this.
    if not os.path.exists(config.source_dir):
        os.makedirs(config.source_dir)
    with open(f'{config.source_dir}/{file_name}', 'wb') as f:
        print(f'Downloading {file_name}...')
        for chunk in res.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
    print('Download completed. Moving files to...')
    move_files()


def move_files() -> None:
    """Function to move files downloaded from one directory to another directory of user's choosing."""
    print("Moving files...")
    match platform.system():
        case 'Linux':
            # Linux needs to move from here to /mnt/d/ which is in Windows.
            print('Linux!')
        case 'Windows':
            ...
        case _:
            ...