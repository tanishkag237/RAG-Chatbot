from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from transformers import pipeline
from langchain_community.llms import HuggingFacePipeline
from langchain.chains import RetrievalQA


def getRAGchain():
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = Chroma(persist_directory="chroma_db3", embedding_function=embedding_model)

    hf_pipeline = pipeline(
        "text2text-generation",
        model="MBZUAI/LaMini-Flan-T5-783M",  # or flan-t5-small
        max_new_tokens=256,
        temperature=0.2,
    )

    llm = HuggingFacePipeline(pipeline=hf_pipeline)

    # converts vector store into a retriever
    # finds the top k most similar documents to the query
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3}) 
    rag_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

    return rag_chain        



if __name__ == "__main__":
    rag_chain = getRAGchain()
    while True:
        query = input("\nAsk something (or 'exit'): ")
        if query.lower() == "exit":
            break
        result = rag_chain.invoke({"query": query})
        print("\nAnswer:", result["result"], "\n")