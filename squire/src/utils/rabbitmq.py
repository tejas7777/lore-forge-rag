import pika
from .logger import logger
from ..config import Config

class _RabbitMQConsumer:

    _instance = None
    _initialized = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    

    def __init__(self):
       if not self._initialized:
           self.host = Config.RABBITMQ_HOST
           self.port = Config.RABBITMQ_PORT
           self.queue = Config.RABBITMQ_QUEUE
           self.credentials = pika.PlainCredentials(Config.RABBITMQ_USER, Config.RABBITMQ_PASS)
           self._connection = None
           self._channel = None
           self._initialized = True
           logger.info(f"[rabbitmq][init] Initialized consumer for queue: {self.queue}")

    def connect(self):
        try:
            if self._connection is None or self._connection.is_closed:
                logger.info(f"[rabbitmq][connect] Connecting to {self.host}:{self.port}")
                params = pika.ConnectionParameters(
                    host=self.host,
                    port=self.port,
                    credentials=self.credentials
                )
                self._connection = pika.BlockingConnection(params)
                self._channel = self._connection.channel()
                self._channel.queue_declare(queue=self.queue, durable=True)
                logger.info(f"[rabbitmq][connect] Connected successfully to queue: {self.queue}")
        except Exception as e:
            logger.error(f"[rabbitmq][connect][error] {str(e)}")
            raise e

    def consume(self, callback):
        try:
            logger.info(f"[rabbitmq][consume] Starting consumption from queue: {self.queue}")
            self.connect()
            self._channel.basic_consume(
                queue=self.queue,
                on_message_callback=callback,
                auto_ack=False
            )
            self._channel.start_consuming()
        except Exception as e:
            logger.error(f"[rabbitmq][consume][error] {str(e)}")
            self.close()
            raise e

    def close(self):
        try:
            if self._connection and not self._connection.is_closed:
                logger.info("[rabbitmq][close] Closing connection")
                self._connection.close()
                logger.info("[rabbitmq][close] Connection closed successfully")
        except Exception as e:
            logger.error(f"[rabbitmq][close][error] {str(e)}")
            raise e
        

rabbitMQ = _RabbitMQConsumer()