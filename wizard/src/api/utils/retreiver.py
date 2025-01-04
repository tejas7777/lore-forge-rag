from src.api.utils.logger import get_logger_service
from src.api.utils.embedder import EmbeddingService, get_embedding_service
from src.api.services.elastic import ElasticService, get_es_service
from src.api.config import settings
from fastapi import Depends
from typing import List, Dict, Any

logger = get_logger_service()

def get_retriever_service(
    embedding_service: EmbeddingService = Depends(get_embedding_service),
    es_service: ElasticService = Depends(get_es_service)
):
    if not hasattr(get_retriever_service, "instance"):
        get_retriever_service.instance = RetrieverService(
            embedding_service=embedding_service,
            es_service=es_service
        )
    return get_retriever_service.instance

class RetrieverService:
    def __init__(
        self,
        embedding_service: EmbeddingService,
        es_service: ElasticService
    ):
        self.embedding_service = embedding_service
        self.es_service = es_service
        logger.info("[retriever][init] Initialized Retriever Service")

    async def retrieve(self, query: str) -> Dict[str, Any]:
        try:
            logger.info(f"[retriever][retrieve] Processing query: {query}")

            query_vector = await self.embedding_service.encode_query(query)
            logger.info("[retriever][retrieve] Query encoded successfully")

            similar_chunks = await self.es_service.search_similar(
                query_vector, 
                top_k=settings.TOP_K_CHUNKS
            )
            logger.info(f"[retriever][retrieve] Found {len(similar_chunks)} similar chunks")

            return {
                "query": query,
                "chunks": similar_chunks,
                "metadata": {
                    "chunk_count": len(similar_chunks),
                    "sources": list(set(chunk["doc_id"] for chunk in similar_chunks))
                }
            }

        except Exception as e:
            logger.error(f"[retriever][retrieve][error] Failed to retrieve context: {str(e)}")
            raise e