from src.utils.rabbitmq import rabbitMQ
from src.config import Config
from src.config import Config
from src.utils.logger import logger
from src.utils.mongo import mongoDBUtil
from bson.objectid import ObjectId
import pymongo
from src.embeddings.SentenceEmbedder import SentenceEmbedder

class Consumer:
   def __init__(self):
       self.processor = None
       self.rabbitMQ = rabbitMQ
       self.mongoUtil = mongoDBUtil
       self.rabbitMQ.connect()
       self.sentenceEmbedder = SentenceEmbedder()

   def callback(self, ch, method, properties, body):
        try:
            doc_id = ObjectId(body.decode())
            document = self.mongoUtil.getDocument(doc_id)
            
            if document is None:
                logger.error(f"[consumer][callback][error] Document not found: {doc_id}")
                ch.basic_ack(delivery_tag=method.delivery_tag)
                return
                
            logger.info(f"[consumer][callback] Retrieved document: {document['_id']}")

            ch.basic_ack(delivery_tag=method.delivery_tag)

            self.sentenceEmbedder.process(document)
            
        except (pymongo.errors.NetworkTimeout, pymongo.errors.ConnectionFailure) as e:
            logger.error(f"[consumer][callback][error] Temporary error: {str(e)}")
            ch.basic_nack(delivery_tag=method.delivery_tag)
            
        except Exception as e:
            logger.error(f"[consumer][callback][error] Permanent error: {str(e)}")
            ch.basic_ack(delivery_tag=method.delivery_tag)

   def start(self):
       logger.info("[consumer][start] Starting consumer")
       self.rabbitMQ.consume(self.callback)