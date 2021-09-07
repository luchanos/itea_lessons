import aiohttp

from logging import getLogger, StreamHandler
import sys

logger = getLogger(__name__)

stdout_handler = StreamHandler(sys.stdout)
logger.addHandler(stdout_handler)
logger.setLevel("DEBUG")


class TgClientAsync:
    def __init__(self, token):
        self.token = token
        self.session = None

    async def setup(self):
        self.session = aiohttp.ClientSession()
        logger.info("Telegram client has been set up!")

    async def send_text_message(self, message, chat_id):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={chat_id}&text={message}"

        async with self.session.get(url) as response:
            data = await response.read()
            logger.info(data)
