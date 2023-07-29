import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.chains import LLMChain

# access docs from session state

if "db" not in st.session_state.keys():
    st.error("No docs loaded yet")

# else:
#     st.write(st.session_state.db)

def search_docs(query):
    docs = st.session_state.db.similarity_search(query, k=4)
    docs_content = " ".join([d.page_content for d in docs])
    return docs_content

def query_llm(query):
    docs = search_docs(query)
    response = chain.run(question=query, docs=docs)
    response = response.replace("\n", "")
    return response

# setup llm
# initially don't pass in previous messages

chat = ChatOpenAI(model="gpt-3.5-turbo")

system_template = """
    You are a helpful assistant that can answer questions about the documents provided: {docs}

    Only use the factual information from the transcript to answer the question.

    If you feel like you don't have enough information, say "I don't know".

    Your answers should be verbose and detailed.
"""

system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

human_template = "Answer the following question: {question}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

chain = LLMChain(llm=chat, prompt=chat_prompt)


# app layout
st.title("Custom chatbot 💬")

# with st.chat_message("user"):
#     st.write("Hello 👋")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# syntax checks input is not empty and assigns it
if prompt:= st.chat_input("Say something"):
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        response = query_llm(prompt)
        message_placeholder.markdown(response)

