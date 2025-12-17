import google.generativeai as genai
from typing import List, Optional
from config import settings
from utils.logger import embedding_logger

class GeminiService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)

    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts using Gemini
        """
        embedding_logger.info(f"Generating embeddings for {len(texts)} texts")
        embeddings = []

        for i, text in enumerate(texts):
            try:
                # Use the embed_content method to get embeddings
                result = genai.embed_content(
                    model="models/embedding-001",  # Using the embedding model
                    content=text,
                    task_type="RETRIEVAL_DOCUMENT"
                )

                embeddings.append(result['embedding'])
                embedding_logger.debug(f"Generated embedding {i+1}/{len(texts)}")
            except Exception as e:
                embedding_logger.error(f"Error generating embedding for text: {str(e)}")
                # Append zeros if there's an error
                embeddings.append([0.0] * 768)  # Standard embedding dimension

        embedding_logger.info(f"Successfully generated {len(embeddings)} embeddings")
        return embeddings

    async def generate_response(self, prompt: str) -> str:
        """
        Generate a response using the Gemini model with the provided prompt
        """
        try:
            response = await self.model.generate_content_async(prompt)

            if response and response.text:
                return response.text
            else:
                return "I couldn't generate a response. Please try again."

        except Exception as e:
            embedding_logger.error(f"Error generating response: {str(e)}")
            return "Sorry, I encountered an error while processing your request."

    async def generate_selected_text_response(self, prompt: str, selected_text: str) -> str:
        """
        Generate a response based only on the selected text
        """
        try:
            full_prompt = f"Based only on the following text, please answer the question:\n\nSelected text: {selected_text}\n\nQuestion: {prompt}"

            response = await self.model.generate_content_async(full_prompt)

            if response and response.text:
                return response.text
            else:
                return "I couldn't generate a response. Please try again."

        except Exception as e:
            embedding_logger.error(f"Error generating response: {str(e)}")
            return "Sorry, I encountered an error while processing your request."

    async def generate_response_with_selected_text(self, question: str, selected_text: str) -> str:
        """
        Generate a response using ONLY the selected text as context
        """
        try:
            system_prompt = f"You are an AI assistant for this book. Answer only using the provided text.\n\nProvided Text:\n{selected_text}\n\nQuestion: {question}"

            response = await self.model.generate_content_async(system_prompt)

            if response and response.text:
                return response.text
            else:
                return "I couldn't generate a response. Please try again."

        except Exception as e:
            embedding_logger.error(f"Error generating response: {str(e)}")
            return "Sorry, I encountered an error while processing your request."

# Initialize the service
gemini_service = GeminiService()