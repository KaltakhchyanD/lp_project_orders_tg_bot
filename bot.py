import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler

from settings import PROXY
from handlers import *

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

logger = logging.getLogger(__name__)
logger.info('BOTBOT')



def main():
    mybot = Updater(os.getenv('API_KEY'), request_kwargs=PROXY)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', start_handler, pass_user_data=True))
    dp.add_handler(pizza_menu)


    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()