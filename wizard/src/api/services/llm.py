from typing import Dict, Any
import httpx
from src.api.config import settings
from src.api.utils.logger import get_logger_service

logger = get_logger_service()

def get_llm_service():
    if not hasattr(get_llm_service, "instance"):
        get_llm_service.instance = LLMService()
    return get_llm_service.instance

class LLMService:
    def __init__(self):
        self.base_url = settings.LLM_ENDPOINT
        self.headers = {
            "Content-Type": "application/json"
        }
        logger.info("[llm][init] LLM service initialized")

    async def generate_response(self, query: str, context: list) -> Dict[str, Any]:
        try:
            system_prompt = "You are a helpful AI assistant that answers questions based on the provided context."
            context_text = "\n".join(chunk["text"] for chunk in context)
            
            prompt = f"""Context: {context_text}

Question: {query}

Please answer the question based only on the provided context. If the context doesn't contain enough information to answer the question, please say so."""

            payload = {
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 512,
                "stream": False
            }

            logger.info("[llm][generate] Sending request to LLM")
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/v1/chat/completions",
                    json=payload,
                    headers=self.headers,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    response_data = response.json()
                    generated_text = response_data["choices"][0]["message"]["content"]
                    logger.info("[llm][generate] Successfully generated response")
                    return {"response": generated_text}
                else:
                    raise Exception(f"LLM request failed with status {response.status_code}")

        except Exception as e:
            logger.error(f"[llm][generate][error] Failed to generate response: {str(e)}")
            raise e