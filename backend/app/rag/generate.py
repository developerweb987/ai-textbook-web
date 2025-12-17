from typing import List, Dict
import google.generativeai as genai
from config import settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure the Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)

# Initialize the generative model
model = genai.GenerativeModel(
    model_name=settings.GEMINI_MODEL if hasattr(settings, 'GEMINI_MODEL') else 'gemini-1.5-flash',
    generation_config={
        "temperature": 0.7,
        "max_output_tokens": 2000,
    }
)

async def generate_response(user_query: str, retrieved_docs: List[Dict]) -> str:
    """
    Generate a response using the Gemini model based on the user query and retrieved documents
    """
    try:
        # Format the context from retrieved documents
        context_parts = []
        for doc in retrieved_docs:
            context_parts.append(doc['text'])

        context = "\n\n".join(context_parts)

        # Create a prompt that combines the user query with the retrieved context
        if context:
            prompt = f"""
            Answer ONLY from the retrieved book content.

            Book Content:
            {context}

            Question: {user_query}

            Answer:
            """
        else:
            prompt = f"""
            Answer ONLY from the retrieved book content.

            I don't have relevant content from the book to answer your question: {user_query}
            """

        # Generate response using the model
        response = await model.generate_content_async(prompt)

        # Extract the text response
        if response and response.text:
            return response.text.strip()
        else:
            return "I couldn't generate a response based on the provided book content."

    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        raise

async def generate_response_from_selected_text(user_query: str, selected_text: str) -> str:
    """
    Generate a response using only the selected text as context
    """
    try:
        # Create a prompt that uses only the selected text as context
        prompt = f"""
        Answer ONLY from the provided text.

        Provided Text:
        {selected_text}

        Question: {user_query}

        Answer:
        """

        # Generate response using the model
        response = await model.generate_content_async(prompt)

        # Extract the text response
        if response and response.text:
            return response.text.strip()
        else:
            return "I couldn't generate a response based on the provided text."

    except Exception as e:
        logger.error(f"Error generating response from selected text: {str(e)}")
        raise

async def generate_summary(text: str, max_length: int = 300) -> str:
    """
    Generate a summary of the given text
    """
    try:
        prompt = f"""
        Please provide a concise summary of the following text in no more than {max_length} characters:

        Text: {text}

        Summary:
        """

        response = await model.generate_content_async(prompt)

        if response and response.text:
            return response.text.strip()
        else:
            return "Could not generate a summary."

    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
        raise

async def generate_followup_questions(user_query: str, retrieved_docs: List[Dict], num_questions: int = 3) -> List[str]:
    """
    Generate follow-up questions based on the user query and retrieved documents
    """
    try:
        # Format the context from retrieved documents
        context_parts = []
        for doc in retrieved_docs:
            context_parts.append(doc['text'])

        context = "\n\n".join(context_parts)

        prompt = f"""
        Based on the following context and user question, generate {num_questions} relevant follow-up questions.
        Return only the questions, one per line, without any additional text.

        Context:
        {context}

        User Question: {user_query}
        """

        response = await model.generate_content_async(prompt)

        if response and response.text:
            # Split the response into individual questions
            questions = [q.strip() for q in response.text.strip().split('\n') if q.strip()]
            # Filter out any non-question text
            questions = [q for q in questions if '?' in q or q.startswith(('What', 'How', 'Why', 'When', 'Where', 'Who', 'Which'))]
            return questions[:num_questions]
        else:
            return []

    except Exception as e:
        logger.error(f"Error generating follow-up questions: {str(e)}")
        return []