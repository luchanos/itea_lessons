import sys
from logging import getLogger, StreamHandler

logger = getLogger(__name__)
logger.setLevel("DEBUG")

stdout_handler = StreamHandler(sys.stdout)
logger.addHandler(stdout_handler)

logger.error("Ошибка!")
logger.warning("Ворнинг!")
logger.info("Инфо уровень!")
logger.debug("Дебаг уровень!")
