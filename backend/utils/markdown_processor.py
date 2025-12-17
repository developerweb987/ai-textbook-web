import os
import re
import tiktoken
from pathlib import Path
from typing import List, Dict, Tuple
from slugify import slugify
import yaml
from utils.logger import app_logger

def read_markdown_files(docs_path: str) -> List[Dict]:
    """
    Read all markdown files from the docs directory and return a list of documents
    """
    app_logger.info(f"Reading markdown files from: {docs_path}")
    documents = []
    docs_dir = Path(docs_path)

    # Look for markdown files with various extensions
    md_extensions = ['*.md', '*.mdx']

    files_found = 0
    for ext in md_extensions:
        for file_path in docs_dir.rglob(ext):
            if file_path.is_file():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Extract frontmatter if present
                    frontmatter = {}
                    content_without_frontmatter = content

                    # Check for YAML frontmatter
                    if content.startswith('---'):
                        parts = content.split('---', 2)
                        if len(parts) >= 3:
                            try:
                                frontmatter = yaml.safe_load(parts[1])
                                content_without_frontmatter = parts[2]
                            except yaml.YAMLError:
                                # If YAML parsing fails, treat as regular content
                                app_logger.warning(f"Failed to parse frontmatter in {file_path}")
                                pass

                    # Clean up the content
                    clean_content = clean_markdown(content_without_frontmatter)

                    document = {
                        'id': str(file_path),
                        'path': str(file_path.relative_to(docs_dir)),
                        'filename': file_path.name,
                        'content': clean_content,
                        'frontmatter': frontmatter,
                        'source_url': f"/docs/{file_path.relative_to(docs_dir).as_posix()}"  # Assuming Docusaurus URL structure
                    }

                    documents.append(document)
                    files_found += 1
                except Exception as e:
                    app_logger.error(f"Error reading {file_path}: {str(e)}")

    app_logger.info(f"Successfully read {files_found} markdown files")
    return documents

def clean_markdown(content: str) -> str:
    """
    Clean markdown content by removing unnecessary elements
    """
    # Remove HTML comments
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)

    # Remove extra whitespace
    content = re.sub(r'\n\s*\n', '\n\n', content)

    # Remove leading/trailing whitespace
    content = content.strip()

    return content

def extract_headings(content: str) -> List[Dict]:
    """
    Extract headings from markdown content
    """
    # Pattern to match markdown headings (## Heading, ### Heading, etc.)
    heading_pattern = r'^(#{1,6})\s+(.+)$'
    lines = content.split('\n')
    headings = []

    for line_num, line in enumerate(lines):
        match = re.match(heading_pattern, line.strip())
        if match:
            headings.append({
                'level': len(match.group(1)),  # Number of # symbols
                'text': match.group(2).strip(),
                'line_number': line_num
            })

    return headings

def chunk_text(text: str, chunk_size_tokens: int = 700) -> List[Dict]:
    """
    Split text into chunks based on token count
    """
    app_logger.debug(f"Chunking text of length {len(text)} with max tokens {chunk_size_tokens}")
    tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")

    # Split text into sentences to avoid cutting in the middle of sentences
    sentences = re.split(r'[.!?]+\s+', text)

    chunks = []
    current_chunk = ""
    current_tokens = 0

    for sentence in sentences:
        # Estimate tokens for the sentence
        sentence_tokens = len(tokenizer.encode(sentence))

        # If a single sentence is too long, split it by length
        if sentence_tokens > chunk_size_tokens:
            # Split the long sentence into smaller pieces
            words = sentence.split()
            temp_chunk = ""

            for word in words:
                temp_chunk += word + " "

                # Check if adding this word makes the chunk too long
                temp_tokens = len(tokenizer.encode(temp_chunk))

                if temp_tokens > chunk_size_tokens:
                    # Save the current chunk and start a new one
                    if current_chunk.strip():
                        chunks.append({
                            'text': current_chunk.strip(),
                            'tokens': current_tokens
                        })

                    current_chunk = word + " "
                    current_tokens = len(tokenizer.encode(current_chunk))
                    temp_chunk = current_chunk
                else:
                    current_chunk = temp_chunk
                    current_tokens = temp_tokens

            # Add remaining content to current chunk
            if temp_chunk.strip() != word + " ":
                current_chunk = temp_chunk
                current_tokens = len(tokenizer.encode(temp_chunk))
        else:
            # Check if adding this sentence would exceed the chunk size
            total_tokens = current_tokens + sentence_tokens

            if total_tokens <= chunk_size_tokens:
                current_chunk += sentence + ". "
                current_tokens = len(tokenizer.encode(current_chunk))
            else:
                # Save the current chunk and start a new one
                if current_chunk.strip():
                    chunks.append({
                        'text': current_chunk.strip(),
                        'tokens': current_tokens
                    })

                current_chunk = sentence + ". "
                current_tokens = len(tokenizer.encode(current_chunk))

    # Add the last chunk if it has content
    if current_chunk.strip():
        chunks.append({
            'text': current_chunk.strip(),
            'tokens': current_tokens
        })

    app_logger.debug(f"Text chunked into {len(chunks)} chunks")
    return chunks

def process_documents(docs_path: str, chunk_size_tokens: int = 700) -> List[Dict]:
    """
    Process documents: read markdown files and chunk them
    """
    app_logger.info(f"Processing documents from {docs_path} with chunk size {chunk_size_tokens}")
    documents = read_markdown_files(docs_path)
    processed_docs = []

    for doc in documents:
        # Extract headings from the document
        headings = extract_headings(doc['content'])

        # Create chunks for the document
        chunks = chunk_text(doc['content'], chunk_size_tokens)

        for i, chunk in enumerate(chunks):
            # Find the most relevant heading for this chunk based on position
            chunk_start_line = doc['content'][:doc['content'].find(chunk['text'])].count('\n') if chunk['text'] in doc['content'] else 0
            relevant_heading = ""

            # Find the heading that appears before this chunk
            for heading in reversed(headings):
                if heading['line_number'] <= chunk_start_line:
                    relevant_heading = heading['text']
                    break

            processed_doc = {
                'id': f"{doc['path']}_chunk_{i}",
                'document_id': doc['path'],
                'filename': doc['filename'],
                'content': chunk['text'],
                'tokens': chunk['tokens'],
                'metadata': {
                    'source': doc['source_url'],
                    'path': doc['path'],
                    'filename': doc['filename'],
                    'chunk_index': i,
                    'total_chunks': len(chunks),
                    'section_heading': relevant_heading,
                    **doc.get('frontmatter', {})
                }
            }
            processed_docs.append(processed_doc)

    app_logger.info(f"Processed {len(documents)} documents into {len(processed_docs)} chunks")
    return processed_docs