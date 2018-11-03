import logging
import os

import sentry_sdk
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler

from handlers import conversation
from settings import PROXY


logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO
#                    filename='bot.log'
                    )

logger = logging.getLogger(__name__)
logger.info('BOTBOT')

sentry_sdk.init("https://b67a03c0cb244e35b5a57c803abae167@sentry.io/1315096")



def main():
    mybot = Updater(os.getenv('API_KEY'), request_kwargs=PROXY)
    dp = mybot.dispatcher
    dp.add_handler(conversation)


    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
