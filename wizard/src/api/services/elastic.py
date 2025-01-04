from typing import List, Dict, Any
from elasticsearch import AsyncElasticsearch
from src.api.config import settings
from src.api.utils.logger import get_logger_service
import numpy as np


logger = get_logger_service()

def get_es_service():
   if not hasattr(get_es_service, "instance"):
       get_es_service.instance = ElasticService()
   return get_es_service.instance

class ElasticService:
   def __init__(self):
       self.es = AsyncElasticsearch([
           f"{settings.VECTOR_DB_SCHEME}://{settings.VECTOR_DB_HOST}:{settings.VECTOR_DB_PORT}"
       ])
       self.index = settings.VECTOR_DB_INDEX
       logger.info("[elastic][init] Connected to Elasticsearch")
       
       
   async def search_similar(
        self, 
        query_vector: np.ndarray, 
        top_k: int = 5,
        min_score: float = 0.7,
        include_metadata: bool = True
    ) -> List[Dict[str, Any]]:

        try:
            logger.info(f"[elastic][search] Searching for top {top_k} similar chunks")


            query = {
                "query": {
                    "script_score": {
                        "query": {"match_all": {}},  # Changed from bool query
                        "script": {
                            "source": "cosineSimilarity(params.query_vector, 'vector') + 1.0",
                            "params": {
                                "query_vector": query_vector.tolist()
                            }
                        }
                    }
                },
                "size": top_k,
                "_source": ["text", "doc_id", "metadata"] if include_metadata else ["text"]
            }

            response = await self.es.search(
                index=self.index,
                body=query
            )

            results = []
            for hit in response["hits"]["hits"]:
                result = {
                    "text": hit["_source"]["text"],
                    "score": hit["_score"] - 1.0,
                }
                
                if include_metadata:
                    result.update({
                        "doc_id": hit["_source"]["doc_id"],
                        "metadata": hit["_source"]["metadata"]
                    })

                results.append(result)

            logger.info(f"[elastic][search] Found {len(results)} chunks above threshold")
            return results

        except Exception as e:
            logger.error(f"[elastic][search][error] Search failed: {str(e)}")
            raise e

   async def close(self):
       await self.es.close()