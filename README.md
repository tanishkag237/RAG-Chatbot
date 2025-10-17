1. app.py

-> Load .md/.txt file using langchain_community.document_loaders (UnstructuredMarkdownLoader, TextLoader)

-> Split document into chunks using RecursiveCharacterTextSplitter

-> Use sentence-transformers/all-MiniLM-L6-v2 model to create embeddings and Chroma vector store to store the embeddings

2. chatbot.py

-> load the embeddings and vector store again

-> use MBZUAI/LaMini-Flan-T5-783M LLM model (flan-t5-small -> doesn't generate good responses. mistralai/Mistral-7B-Instruct-v0.2 -> very heavy)

-> Creates a retrieval-augmented QA chain (RAG) that uses:
llm — your HuggingFacePipeline model to generate text.
retriever — the Chroma vectorstore retriever that fetches relevant docs (search_kwargs={"k":3} → top 3).
chain_type="stuff" — a simple strategy that "stuffs" all retrieved docs into the prompt given to the LLM.

-> while True / input loop:

Repeatedly prompt the user for a query (or "exit" to stop).
If the user types "exit", break the loop.
result = rag_chain.invoke({"query": query}):

Calls the chain with a dict input (invoke returns a dict of outputs).
For RetrievalQA the chain returns an output key "result" containing the answer string (and sometimes other keys like source_documents depending on config).

// Working for gemini model rn