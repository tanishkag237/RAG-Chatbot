from langchain_community.document_loaders import PDFPlumberLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

loader2 = PDFPlumberLoader("./data/AWSnotes.pdf")
docs2 = loader2.load()

text_splitter2 = RecursiveCharacterTextSplitter(
    chunk_size=1000,   #
    chunk_overlap=100,  
    length_function=len,  
    separators=["\n\n", "\n", " ", ""]  
)

chunks2 = text_splitter2.split_documents(docs2)

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vectorstore = Chroma.from_documents(
    documents=chunks2,
    embedding=embedding_model,
    persist_directory="chroma_db2"  
)

vectorstore.persist()
print("✅ Chroma vector store created and saved!")


vectorstore = Chroma(persist_directory="chroma_db2", embedding_function=embedding_model)
retriever = vectorstore.as_retriever(search_kwargs={"k": 1})


llm = ChatGoogleGenerativeAI(
    model="models/gemini-2.5-pro",
    temperature=0.7,
    credentials={"api_key": os.getenv("GEMINI_API_KEY")}
     
)

rag_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

while True:
    query = input("\n Ask something (or 'exit'): ")
    if query.lower() == "exit":
        break
    result = rag_chain.invoke({"query": query})
    print("\n🧠 Answer:", result["result"], "\n")