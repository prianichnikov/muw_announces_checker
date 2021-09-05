#!/usr/bin/env python3

import time
import sys
import requests
import os.path
from bs4 import BeautifulSoup

FILE_NAME = 'cache.txt'
PAGE_URL = 'https://www.gov.pl/web/uw-mazowiecki/biezace-informacje-wsc'

TG_API_URL = 'https://api.telegram.org/bot'
TG_BOT_TOKEN = ''
TG_CHAT_ID = ''


def log(message):
    now = time.strftime('%Y-%m-%d %H:%M:%S')
    print(now + ' ' + message)


def load_page():
    response = requests.get(PAGE_URL)
    if response.status_code != 200:
        log("Can't load announces page, response code: {}".format(response.status_code))
        sys.exit(1)
    soup = BeautifulSoup(response.text, 'html.parser')
    titles = soup.find_all("div", {"class": "title"})
    message = ''
    i = 1
    log('Found {} announces'.format(len(titles)))
    for title in titles:
        message = message + '{}) '.format(i) + title.get_text() + '\n'
        i += 1
    return message


def read_file():
    text = ''
    if os.path.isfile(FILE_NAME):
        f = open(FILE_NAME, 'r', encoding='utf8')
        text = f.read()
        f.close()
    else:
        write_file(FILE_NAME, text)
    return text


def write_file(file_name, text):
    f = open(file_name, 'w', encoding='utf8')
    f.write(text)
    f.close()


def send_tg_message(message):
    url = TG_API_URL + TG_BOT_TOKEN + '/sendMessage'
    payload = {'chat_id': TG_CHAT_ID, 'text': message}
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        log('Could not send Telegram message, status code: {}, exit'.format(response.status_code))
        sys.exit(1)


if __name__ == "__main__":
    text_from_page = load_page()
    text_from_file = read_file()
    if text_from_page != text_from_file:
        log('Announces were changed, sending message')
        write_file(FILE_NAME, text_from_page)
        text_from_page = 'New announces on the page ' + PAGE_URL + '\n\n' + text_from_page
        send_tg_message(text_from_page)
    else:
        log("Announces weren't changed")

    sys.exit(0)
