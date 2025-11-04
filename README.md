# Clinical RAG Assistant

Project Summary

This project is a high-speed, interactive chatbot that demonstrates a complete, end-to-end Retrieval-Augmented Generation (RAG) pipeline. It transforms a dense, 160-page PDF textbook ("Health Case Studies" by BCcampus) into a secure, searchable, and intelligent web application.

Users can ask complex questions about the medical cases in natural language, and the application instantly retrieves the most relevant information from the text and generates a concise, accurate answer.

This project showcases the entire data lifecycle: from raw PDF extraction and cleaning, through vector embedding and database storage, to a secure, real-time streaming frontend.

# Key Features & Tech Stack

This application was built using the following technologies:

Frontend (UI): Streamlit (for the interactive chat interface)

LLM (Generation): Groq API (using llama-3.1-8b-instant for high-speed, streaming responses)

Vector Database (Retrieval): ChromaDB (for efficient, local vector storage and similarity search)

Embedding Model: SentenceTransformers (all-MiniLM-L6-v2 to convert text into vector embeddings)

Data Pipeline:

PyMuPDF: For extracting raw text from the original PDF.

LangChain (Text-Splitters): For cleaning and splitting the text into uniform, overlapping chunks.

Security & Environment: python-dotenv (for secure API key management outside of source control) and Git/GitHub.

# Core Data Pipeline

The application is powered by a 4-step data pipeline:

Extract: Raw text is extracted from the Health-Case-Studies-....pdf using extract_all.py.

Chunk: The text is cleaned, and RecursiveCharacterTextSplitter is used to create over 150 small, 1000-character text chunks.

Embed: Each text chunk is converted into a vector embedding and stored in a local ChromaDB database using embed_and_store.py.

Retrieve & Generate (app.py):
a.  The user's question is vectorized in real-time.

b.  ChromaDB is queried to find the top 5 most relevant text chunks.

c.  The question and these 5 chunks are sent as context to the Groq API.

d.  The LLM's answer is streamed back to the Streamlit app instantly.

# Demo
![Image](https://github.com/user-attachments/assets/9d2860f2-d372-4f27-92e6-dd440e4e9be9)
![Image](https://github.com/user-attachments/assets/ae6f1be3-b155-40c0-9d81-cdba61cf666a)

# Full Video 
https://github.com/user-attachments/assets/2a21bce4-c185-4d70-a6ee-ddfb26ab9915
