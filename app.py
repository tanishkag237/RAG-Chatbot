# from langchain_community.document_loaders import PDFPlumberLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import UnstructuredMarkdownLoader

loader = UnstructuredMarkdownLoader("./data/info.md")
docs = loader.load()
print(docs[0])

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,   #
    chunk_overlap=100,  
    length_function=len,  
    separators=["\n\n", "\n", " ", ""]  
)

chunks = text_splitter.split_documents(docs)

print(f"Number of chunks: {len(chunks)}")
print(chunks[0]) 

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory="chroma_db"  
)

vectorstore.persist()
print("✅ Chroma vector store created and saved!")