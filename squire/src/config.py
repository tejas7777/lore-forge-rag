from dataclasses import dataclass

@dataclass
class Config:
   RABBITMQ_HOST: str = "localhost"
   RABBITMQ_PORT: int = 5672
   RABBITMQ_QUEUE: str = "rag_queue"
   RABBITMQ_USER: str = "guest"
   RABBITMQ_PASS: str = "guest"

   MONGODB_URI: str = "mongodb://localhost:27017"
   MONGODB_DB: str = "loresmaster"
   MONGODB_COLLECTION: str = "lorestore"

   VECTOR_DB_SCHEME: str = "http"
   VECTOR_DB_HOST: str = "localhost"
   VECTOR_DB_PORT: int = 9200
   VECTOR_DB_INDEX:str = "embeddings"


   CHUNK_SIZE: int = 512
   CHUNK_OVERLAP: int = 50
   MODEL_NAME: str = "all-MiniLM-L6-v2"