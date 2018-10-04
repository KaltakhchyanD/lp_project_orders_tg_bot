import logging
import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler

from handlers import conversation
#from pizza_handlers import conversation, start_handler
from settings import PROXY


logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO
#                    filename='bot.log'
                    )

logger = logging.getLogger(__name__)
logger.info('BOTBOT')



def main():
    mybot = Updater(os.getenv('API_KEY'), request_kwargs=PROXY)
    dp = mybot.dispatcher
    dp.add_handler(conversation)


    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()