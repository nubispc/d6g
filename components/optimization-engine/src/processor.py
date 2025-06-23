# processor.py

import asyncio
from library.rabbitmq import consume_messages
import logging

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    connection = loop.run_until_complete(consume_messages())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        logger.info("Processor interrupted, closing connection...")
        exit(0)
    finally:
        loop.run_until_complete(connection.close())
