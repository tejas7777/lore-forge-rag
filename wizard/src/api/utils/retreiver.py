from src.api.utils.logger import get_logger_service
from src.api.utils.embedder import EmbeddingService, get_embedding_service, get_cross_encoder
from src.api.services.elastic import ElasticService, get_es_service
from src.api.config import settings
from fastapi import Depends
from typing import List, Dict, Any
from sentence_transformers import CrossEncoder

logger = get_logger_service()

def get_retriever_service(
    embedding_service: EmbeddingService = Depends(get_embedding_service),
    es_service: ElasticService = Depends(get_es_service)
):
    if not hasattr(get_retriever_service, "instance"):
        cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
        get_retriever_service.instance = RetrieverService(
            embedding_service=embedding_service,
            es_service=es_service,
            cross_encoder=cross_encoder
        )
    return get_retriever_service.instance

class RetrieverService:
    def __init__(
        self,
        embedding_service: EmbeddingService,
        es_service: ElasticService,
        cross_encoder: CrossEncoder
    ):
        self.embedding_service = embedding_service
        self.es_service = es_service
        self.cross_encoder = cross_encoder
        logger.info("[retriever][init] Initialized Retriever Service")

    async def retrieve(self, query: str) -> Dict[str, Any]:
        try:
            logger.info(f"[retriever][retrieve] Processing query: {query}")

            query_vector = await self.embedding_service.encode_query(query)

            similar_chunks = await self.es_service.search_similar(
                query_vector, 
                top_k=settings.TOP_K_CHUNKS
            )
            
            logger.info(f"[retriever][retrieve] Found {len(similar_chunks)} similar chunks")
            
            pairs = [[query, chunk["text"]] for chunk in similar_chunks]
            scores = self.cross_encoder.predict(pairs)
            
            for chunk, score in zip(similar_chunks, scores):
                chunk["cross_score"] = float(score)
                
            reranked_chunks = sorted(similar_chunks, key=lambda x: x["cross_score"], reverse=True)
            selected_chunks = reranked_chunks[:settings.TOP_K_CHUNKS]
            
            logger.info(f"[retriever][retrieve] reranking completed")

            return {
                "query": query,
                "chunks": selected_chunks,
                "metadata": {
                    "chunk_count": len(similar_chunks),
                    "sources": list(set(chunk["doc_id"] for chunk in similar_chunks))
                }
            }

        except Exception as e:
            logger.error(f"[retriever][retrieve][error] Failed to retrieve context: {str(e)}")
            raise e