from sentence_transformers import SentenceTransformer
from src.api.config import settings
from src.api.utils.logger import get_logger_service
from src.api.config import settings
from typing import List, Union
import numpy as np

logger = get_logger_service()

def get_embedding_service():
    if not hasattr(get_embedding_service, "instance"):
        get_embedding_service.instance = EmbeddingService()
    return get_embedding_service.instance

class EmbeddingService:
    def __init__(self):
        logger.info(f"[embedding][init] Loading model: {settings.EMBEDDING_MODEL}")
        try:
            self.model = SentenceTransformer(settings.EMBEDDING_MODEL)
            self.normalize_embeddings = True
            logger.info("[embedding][init] Model loaded successfully")
        except Exception as e:
            logger.error(f"[embedding][init][error] Failed to load model: {str(e)}")
            raise e

    async def encode_query(self, query: str) -> np.ndarray:
        try:
            logger.info("[embedding][encode] Processing query")
            embedding = self.model.encode(
                query,
                normalize_embeddings=self.normalize_embeddings
            )
            logger.info(f"[embedding][encode] Query encoded successfully: shape {embedding.shape}")
            return embedding

        except Exception as e:
            logger.error(f"[embedding][encode][error] Failed to encode query: {str(e)}")
            raise e

    async def encode_batch(self, texts: List[str]) -> np.ndarray:
        try:
            logger.info(f"[embedding][batch] Processing batch of {len(texts)} texts")
            embeddings = self.model.encode(
                texts,
                normalize_embeddings=self.normalize_embeddings,
                batch_size=settings.QUERY_BATCH_SIZE
            )
            logger.info(f"[embedding][batch] Batch encoded successfully: shape {embeddings.shape}")
            return embeddings

        except Exception as e:
            logger.error(f"[embedding][batch][error] Failed to encode batch: {str(e)}")
            raise e

    def get_embedding_dimension(self) -> int:
        return self.model.get_sentence_embedding_dimension()