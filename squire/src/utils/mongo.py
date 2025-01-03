import pymongo
from .logger import logger
from ..config import Config


class _MongoDB:

    _instance = None
    _initialised = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance
    
    def __init__(self):
        if self._initialised is None:
            self.client = pymongo.MongoClient(Config.MONGODB_URI)
            self.db = self.client[Config.MONGODB_DB]
            self.collection = self.db[Config.MONGODB_COLLECTION]
            self._initialized = True

            logger.info(f"[mongodb][init] Connected to {Config.MONGODB_DB}.{Config.MONGODB_COLLECTION}")

    def getDocument(self, doc_id):
        try:
            logger.info(f"[mongodb][get] Fetching document: {doc_id}")
            return self.collection.find_one({"_id": doc_id})
        except Exception as e:
            logger.error(f"[mongodb][get][error] {str(e)}")
            raise e
        

mongoDBUtil = _MongoDB()