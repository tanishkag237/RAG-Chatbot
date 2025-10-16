from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from transformers import pipeline
from langchain_community.llms import HuggingFacePipeline
from langchain.chains import RetrievalQA

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = Chroma(persist_directory="chroma_db2", embedding_function=embedding_model)

hf_pipeline = pipeline(
    "text2text-generation",  # for FLAN-T5 models
    model="MBZUAI/LaMini-Flan-T5-783M",  # or flan-t5-small
    max_new_tokens=256,
    temperature=0.2
)

llm = HuggingFacePipeline(pipeline=hf_pipeline)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

rag_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

while True:
    query = input("\n Ask something (or 'exit'): ")
    if query.lower() == "exit":
        break
    result = rag_chain.invoke({"query": query})
    print("\n🧠 Answer:", result["result"], "\n")