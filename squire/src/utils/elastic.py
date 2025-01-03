from elasticsearch import Elasticsearch
from .logger import logger
from src.config import Config
import json

class VectorDB:
   _instance = None
   _initialized = None

   def __new__(cls):
       if cls._instance is None:
           cls._instance = super().__new__(cls)
       return cls._instance
    
   def __init__(self):
       if not self._initialized:
           self.es = Elasticsearch([f"{Config.VECTOR_DB_SCHEME}://{Config.VECTOR_DB_HOST}:{Config.VECTOR_DB_PORT}"])
           self.index = Config.VECTOR_DB_INDEX
           self._initialized = True
           logger.info(f"[vectordb][init] Connected to Elasticsearch")

   def store(self, doc_id, embeddings):
    try:
        bulk_data = []
        for idx, emb in enumerate(embeddings):
            doc_id_str = str(doc_id)
            chunk_id = emb["chunk"].get("chunk_id", idx)
            bulk_data.append({
                "index": {
                    "_index": self.index,
                    "_id": f"{doc_id_str}_{chunk_id}"
                }
            })
            bulk_data.append({
                "doc_id": doc_id_str,
                "text": emb["chunk"]["text"],
                "vector": emb["embedding"].tolist(),
                "metadata": {
                    "doc_id": str(emb["chunk"]["metadata"].doc_id),
                    "timestamp": emb["chunk"]["metadata"].timestamp.isoformat(),
                    "position": emb["chunk"]["metadata"].position
                }
            })
        ndjson_data = "\n".join([json.dumps(item) for item in bulk_data])
        self.es.bulk(body=ndjson_data)
        logger.info(f"[vectordb][store] Stored {len(embeddings)} vectors for doc: {doc_id_str}")
    except Exception as e:
        logger.error(f"[vectordb][store][error] {str(e)}")
        raise e


vectorDB = VectorDB()