#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import logging
import os

from getlatestpostfromthread import get_all_posts_from_thread
from telegram import InlineQueryResultPhoto, InlineQueryResultGif, InlineQueryResultVideo
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from uuid import uuid4


# Enable logging
logging.basicConfig(
    filename='yotsuba.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)
help_content = '''content'''

enabled_threads = '''a,b,c,d,e,f,g,gif,h,
                hr,k,m,o,p,r,s,t,u,v,vg,vr,w,wg,i,ic,
                r9k,s4s,vip,cm,hm,lgbt,y,3,aco,adv,an,asp,bant,
                biz,cgl,ck,co,diy,fa,fit,gd,hc,his,int,jp,lit,mlp,
                mu,n,news,out,po,pol,qst,sci,soc,sp,tg,toy,trv,tv,
                vp,wsg,wsr,x'''.split(',')


def get_telegram_api_token():
    return os.environ['TELEGRAM_API_TOKEN']

def start(bot, update):
    update.message.reply_text('Hi!')


def help(bot, update):
    update.message.reply_text(help_content)


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
