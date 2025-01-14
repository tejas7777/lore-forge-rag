from fastapi import Depends, HTTPException
from src.api.utils.logger import _Logger,get_logger_service
from src.api.services.elastic import ElasticService, get_es_service
from src.api.utils.embedder import EmbeddingService, get_embedding_service
from src.api.services.llm import LLMService, get_llm_service
from src.api.utils.retreiver import RetrieverService, get_retriever_service

def get_query_controller():
    if not hasattr(get_query_controller, "instance"):
        get_query_controller.instance = QueryController()
    return get_query_controller.instance

class QueryController:
   def __init__(self, es_service: ElasticService = Depends(get_es_service), logger: _Logger = Depends(get_logger_service), 
                embedder: EmbeddingService = Depends(get_embedding_service), 
                llm: LLMService = Depends(get_llm_service), 
                retriever: RetrieverService = Depends(get_retriever_service)
                ):
       self.es_service = es_service
       self.logger = logger
       self.embedder = embedder
       self.llm = llm
       self.retriever = retriever
       logger.info("[query_controller][init] Initializing Query Controller")
       pass
   
   async def health(self):
       try:
           self.logger.info("[query_controller][health] Health check requested")
           return {
               "status": 200,
               "message": "success"
           }
           
       except Exception as e:
           self.logger.error(f"[query_controller][health][error] Health check failed: {str(e)}")
           raise HTTPException(status_code=500, detail=str(e))

   async def process_query(self, query: dict):
        try:
            self.logger.info(f"[query_controller][process] Processing query: {query}")
            
            query_text = query.get('text')
            if not query_text:
                raise HTTPException(status_code=400, detail="Query text is required")

            retrieval_result = await self.retriever.retrieve(query_text)
            similar_chunks = retrieval_result["chunks"]

            llm_response = await self.llm.generate_response(
                query=query_text,
                context=similar_chunks
            )

            return {
                "status": "success",
                "query": query_text,
                "context": similar_chunks,
                "llm_response": llm_response["response"],
                "metadata": retrieval_result["metadata"]
            }

        except HTTPException as he:
            self.logger.error(f"[query_controller][process][error] HTTP Error: {str(he)}")
            raise he
        
        except Exception as e:
            self.logger.error(f"[query_controller][process][error] Query processing failed: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))