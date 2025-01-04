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
            context_text = "\n".join(chunk["text"] for chunk in context)
            system_prompt = """You are a narrative context analyzer focused on maintaining consistency and authenticity. You must:
            - Use only information from provided context
            - Preserve established themes and internal logic
            - Reference specific elements and locations
            - Acknowledge limitations in given information
            - Avoid fabricating details"""

            prompt = f"""Based on the provided material, generate a response that:
            1. Integrates established elements and locations
            2. References existing systems and hierarchies
            3. Acknowledges consequences and limitations
            4. Uses source-specific terminology
            5. Maintains the material's tone

            Context: {context_text}
            Question: {query}"""

            payload = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 512
            }
            
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