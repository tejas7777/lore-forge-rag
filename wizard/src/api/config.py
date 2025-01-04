from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Elasticsearch Config
    VECTOR_DB_SCHEME: str = "http"
    VECTOR_DB_HOST: str = "localhost"
    VECTOR_DB_PORT: int = 9200
    VECTOR_DB_INDEX: str = "embeddings"
    
    # Embedding Model Config
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    
    # LLM Config
    LLM_ENDPOINT: str = "http://localhost:8000"
    QUERY_BATCH_SIZE: int = 64
    TOP_K_CHUNKS:int = 5

    
    class Config:
        env_file = ".env"

settings = Settings()