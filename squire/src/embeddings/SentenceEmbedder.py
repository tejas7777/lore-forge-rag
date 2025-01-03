from sentence_transformers import SentenceTransformer
from dataclasses import dataclass
import numpy as np
from src.utils.logger import logger
import datetime
from src.utils.elastic import vectorDB

@dataclass
class ChunkMetadata:
   doc_id: str
   timestamp: datetime
   position: int

   def to_dict(self):
        return {
            "doc_id": str(self.doc_id),  # Convert ObjectId to string
            "timestamp": self.timestamp.isoformat(),  # Convert datetime to string
            "position": self.position
        }

class Chunker:
   def __init__(self, chunk_size=512, overlap=50):
       self.chunk_size = chunk_size
       self.overlap = overlap

   def chunk_document(self, document):
       content = document['content'].decode()
       chunks = []
       
       paragraphs = content.split('\n')
       current_chunk = ""
       position = 0
       
       for paragraph in paragraphs:
           if len(current_chunk) + len(paragraph) <= self.chunk_size:
               current_chunk += paragraph + "\n"
           else:
               if current_chunk:
                   chunks.append({
                       "text": current_chunk,
                       "metadata": ChunkMetadata(
                           doc_id=document['_id'],
                           timestamp=document['uploadedAt'],
                           position=position
                       )
                   })
                   position += 1
               overlap_text = current_chunk[-self.overlap:] if self.overlap > 0 else ""
               current_chunk = overlap_text + paragraph + "\n"
       
       if current_chunk:
           chunks.append({
               "text": current_chunk,
               "metadata": ChunkMetadata(
                   doc_id=document['_id'],
                   timestamp=document['uploadedAt'],
                   position=position
               )
           })
           
       return chunks

class SentenceEmbedder:
   def __init__(self):
       self.chunker = Chunker()
       logger.info("[embedder][init] Loading model: all-MiniLM-L6-v2")
       self.model = SentenceTransformer('all-MiniLM-L6-v2')

   def process(self, document):
       try:
           logger.info(f"[embedder][process] Processing document: {document['_id']}")
           chunks = self.chunker.chunk_document(document)
           embeddings = []
           
           for chunk in chunks:
               embedding = self.model.encode(chunk['text'])
               embeddings.append({
                   "embedding": embedding,
                   "chunk": chunk
               })
           


           vectorDB.store(document['_id'], embeddings)
           
           logger.info(f"[embedder][process][success] id {str(document['_id'])}")

           return embeddings
    
           
       except Exception as e:
           logger.error(f"[embedder][process][error] {str(e)}")
           raise e