# Multi-Document RAG Chatbot

A Streamlit-based chatbot that enables **retrieval-augmented generation (RAG)** over multiple PDF documents.  
Users can upload PDFs, which are processed into embeddings and stored in **ChromaDB** for retrieval. Queries are then answered using **Google Gemini APIs**, grounding responses in the provided documents.

---

## Features
- **Multi-PDF Uploads** – Upload and process multiple documents at once.  
- **RAG Pipeline** – Embeds documents into ChromaDB and retrieves relevant chunks for each query.  
- **Chat Interface** – Streamlit-powered conversational UI.  
- **Fresh Start Each Run** – Chroma index is built per session (PDFs aren’t persisted across runs).  
- **Gemini LLM Integration** – Uses Gemini API for generating context-grounded answers.

---
