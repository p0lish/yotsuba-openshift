#!/usr/bin/python
import json
import random
import socket

import requests
import urllib3
from bs4 import BeautifulSoup
from requests import HTTPError

from logger import getLogger

POSSIBLE_ERRORS = (HTTPError,
                   socket.error,
                   requests.exceptions.InvalidSchema,
                   requests.exceptions.ConnectionError)

ROOT_URL = "https://boards.4chan.org"
API_URL = "https://api.4chan.org"
IMAGES_URL = "https://i.4cdn.org"
BOARDS_URL = "https://a.4cdn.org/boards.json"
USERAGENTS = [
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201"
]



logger = getLogger('yotsuba-bot', '/home/yotsuba/yotsuba.log')


def random_user_agent():
    return random.choice(USERAGENTS)

USER_AGENT = random_user_agent()


def get_content(url):
    try:
        req = requests.get(url, headers={'User-Agent': USER_AGENT}, verify=False, timeout=20)
        if req.status_code == 200:
            return req.content
    except POSSIBLE_ERRORS as error:
        print(url)
        print("This url causes the following error:", error)
        return ""
    except requests.exceptions.Timeout:
        return "timeout"


def get_boards():
    board_infos = []
    content = get_content(BOARDS_URL).decode('utf-8')
    boards = json.loads(content).get('boards', [])
    for board in boards:
        board_info = {
            "board": board.get("board", ''),
            "title": board.get("title", ''),
            "meta_description": board.get("meta_description", '')
        }
        board_infos.append(board_info)
    return board_infos



def get_boards_list():
    board_list = []
    content = get_content(BOARDS_URL).decode('utf-8')
    boards = json.loads(content).get('boards', [])
    for board in boards:
        board_letter =board.get("board", '')
        if board_letter:
            board_list.append(str(board_letter))
    return board_list




def get_image_url(thread, filename, extension):
    return IMAGES_URL + "/" + thread + "/" + filename  + extension


def get_image_thumbnail(thread, filename, extension):
    return IMAGES_URL + "/" + thread + "/" + filename + 's' + extension


def get_thread_url(thread, thread_no):
    return "/".join((ROOT_URL, thread, "thread",  str(thread_no)))


def get_all_posts_from_thread(thread):
    allPosts = []

    current_url = "/".join((API_URL, thread, "catalog.json"))
    content = json.loads(get_content(current_url).decode('utf-8'))
    for pages in content:
        for threads in pages['threads']:
            if "tim" in threads:
                image_url = get_image_url(thread, str(threads["tim"]), threads["ext"])
                timestamp = threads['time']
                thumbnail = get_image_thumbnail(thread, str(threads["tim"]), threads["ext"])
                link = get_thread_url(thread, threads['no'])
                quote = threads.get('com', '')
                allPosts.append({
                    "timestamp": timestamp,
                    "thumbnail": thumbnail,
                    "image": image_url,
                    "link": link,
                    "description": quote
                })

    sorted_posts = sorted(allPosts, key=lambda k: k['timestamp'], reverse=True)
    logger.info('number of posts in {} thread: {}'.format(thread, len(allPosts)))
    return sorted_posts



get_boards_list()
