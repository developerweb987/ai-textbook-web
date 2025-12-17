# Example usage of the Physical AI Textbook RAG Backend
import asyncio
import aiohttp
import json

async def example_usage():
    base_url = "http://localhost:8000/api/v1"

    # Example 1: Ingest documents
    print("=== Example 1: Ingesting documents ===")
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{base_url}/ingest",
            json={"docs_path": "../frontend/docs"}
        ) as response:
            result = await response.json()
            print(f"Ingestion result: {result}")

    # Example 2: Chat with RAG
    print("\n=== Example 2: Chat with RAG ===")
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{base_url}/chat",
            json={
                "message": "What is physical AI?",
                "session_id": "example-session-1"
            }
        ) as response:
            result = await response.json()
            print(f"Chat response: {json.dumps(result, indent=2)}")

    # Example 3: Chat with selected text
    print("\n=== Example 3: Chat with selected text ===")
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{base_url}/chat/selected-text",
            json={
                "message": "Explain this concept",
                "selected_text": "Physical AI is an interdisciplinary field that combines robotics, machine learning, and control theory to create intelligent systems that interact with the physical world.",
                "session_id": "example-session-2"
            }
        ) as response:
            result = await response.json()
            print(f"Selected text response: {json.dumps(result, indent=2)}")

    # Example 4: Get chat sessions
    print("\n=== Example 4: Get chat sessions ===")
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{base_url}/chat/sessions") as response:
            result = await response.json()
            print(f"Chat sessions: {json.dumps(result, indent=2)}")

if __name__ == "__main__":
    asyncio.run(example_usage())