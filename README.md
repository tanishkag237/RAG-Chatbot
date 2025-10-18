# RAG Based Chatbot

## _About files_
## 1. app.py

- Load .md/.txt file using langchain_community.document_loaders (UnstructuredMarkdownLoader, TextLoader,PDFPlumberLoader)

- Split document into chunks using RecursiveCharacterTextSplitter

- Use sentence-transformers/all-MiniLM-L6-v2 model to create embeddings and Chroma vector store to store the embeddings

## 2. chatbot.py
- Create a function and : 

-  Load the embeddings and vector store again

- use MBZUAI/LaMini-Flan-T5-783M LLM model (flan-t5-small -> doesn't generate good responses. mistralai/Mistral-7B-Instruct-v0.2 -> very heavy)

- Creates a retrieval-augmented QA chain (RAG) that uses:
 - llm — your HuggingFacePipeline model to generate text.
 - retriever — the Chroma vectorstore retriever that fetches relevant docs (search_kwargs={"k":3} → top 3).
 - chain_type="stuff" — a simple strategy that "stuffs" all retrieved docs into the prompt given to the LLM.

## 3. chat_ui.py

- Import streamlit and getRAGchain() function to set up RAG model (embedding + retriever + LLM chain)

- Get user input, call the model to get and answer and save the chat history


> Working on gemini model rn