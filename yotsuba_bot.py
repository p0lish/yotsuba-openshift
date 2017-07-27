#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import logging
import os

from getlatestpostfromthread import get_all_posts_from_thread, get_boards_list, get_boards
from telegram import InlineQueryResultPhoto, InlineQueryResultGif, InlineQueryResultVideo
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from uuid import uuid4


# Enable logging
logging.basicConfig(
    filename='/home/yotsuba/yotsuba.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


enabled_threads = get_boards_list()
BOARD_LIST = get_boards()
help_content = ['''
There are the list of the usable boards, 
just type the board name after the bot name, 
and wait while the images are not available:
''']

stash = ""
for board_item in BOARD_LIST:
        stash += "{board} {tab} {title}".format(board=board_item['board'], tab='\t\t\t',  title=board_item['title']+'\n')
help_content.append(stash)





def get_telegram_api_token():
    return os.environ['TELEGRAM_API_TOKEN']

def start(bot, update):
    update.message.reply_text('hi!')


def help(bot, update, pass_args=True):
    for idx, content in enumerate(help_content):
        update.message.reply_text(help_content[idx])




def get_photo_results(post):
    return InlineQueryResultPhoto(
        id=uuid4(),
        thumb_url=post["thumbnail"],
        photo_url=post["image"],
        caption=post["link"]
    )


def get_gif_results(post):
    return InlineQueryResultGif(
        id=uuid4(),
        thumb_url=post["thumbnail"],
        gif_url=post["image"],
        caption=post["link"]
    )


def get_webm_results(post):
    logger.info(post)
    result = InlineQueryResultGif(
        id=uuid4(),
        thumb_url=post["thumbnail"].replace(".webm", ".jpg"),
        gif_url=post["image"],
        caption=post["link"]
    )
    return result



def inline_query(bot, update):
    query = update.inline_query.query
    logger.info("Query from: " + query)
    results = list()
    if query in enabled_threads:
        posts = get_all_posts_from_thread(query)
        for post in posts:
            if post["image"].endswith('.jpg'):
                results.append(get_photo_results(post))
            if post["image"].endswith('.gif'):
                results.append(get_gif_results(post))
    update.inline_query.answer(results)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(get_telegram_api_token())

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    dp.add_handler(InlineQueryHandler(inline_query))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
