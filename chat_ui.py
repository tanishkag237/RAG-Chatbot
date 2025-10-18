import streamlit as st
from chatbot import getRAGchain

st.title("RAG Chatbot ")

@st.cache_resource # to cache the loaded chain
def load_chain():
    return getRAGchain()

rag_chain = load_chain()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_query = st.chat_input("Ask your question...")

if user_query:
    with st.spinner("Thinking..."):
        result = rag_chain.invoke({"query": user_query})
        answer = result["result"]

    st.session_state.chat_history.append(("You", user_query))
    st.session_state.chat_history.append(("Bot", answer))

# display chat history
for role, msg in st.session_state.chat_history:
    with st.chat_message("user" if role == "You" else "assistant"):
        st.markdown(msg)