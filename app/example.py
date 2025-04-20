import logging

logger = logging.getLogger("app")


def main():
    logger.info("Старт")

    logger.debug("Что то тут")
    logger.debug("Что то там")

    try:
        logger.info("Сейчас буду делить на ноль")
        1 / 0
        logger.critical("Смог поделить на ноль💀💀💀")
    except ZeroDivisionError as error:
        logger.error("Поймал что то except блоке")
        logger.warning("Печатаю ошибку: %s", error)
        logger.warning("Печатаю exc_info", exc_info=True)
        logger.warning("Печатаю stack_info", stack_info=True)
        logger.exception("Печатаю из метода exception")

    logger.info("Завершение работы")
