import streamlit as st


def main():
    st.set_page_config(page_title="Custom chatbot 💬")
    st.title("Home")
    st.write(
        "Welcome to Custom Chatbot where you can create a personalised chatbot by providing documents for its knowledge base as well as a unique system prompt"
    )
    st.write(
        "This website is still in development so if you have any comments please let me know!"
    )
    st.header("Instructions")
    st.subheader("1. Add OpenAI api key")
    st.write(
        "This website makes use of the OpenAI api so you will need to provide your api key for this to work. You can do so in the sidebar"
    )
    st.subheader("2. Add Docs")
    st.write(
        "Now you can move on to the Add Docs page where you can unsurprisingly add docs. Here you can upload text/csv docs, youtube urls, pdfs and more to come soon! You can add multiple documents and when you are done you can submit your docs. If you have already submitted docs before you can load them as well."
    )
    st.subheader("3. Add a System Prompt(Optional)")
    st.write(
        "Nearly ready! Head over to Chatbot where you can a system prompt if you want to. This allows you to further personalise your chabot by describing how exactly you want the bot to chat."
    )
    st.subheader("4. Start Chatting! 💬")
    st.write("You're all set! Start chatting with your own personalised chatbot!")

    with st.sidebar:
        api_key = st.text_input("OpenAI api key", type="password")
        # st.write(api_key)

        # if "api_key" in st.session_state.keys():
        #     api_key = st.session_state.api_key

        if not api_key:
            st.error("Please enter your api key")
        else:
            st.session_state.api_key = api_key


if __name__ == "__main__":
    main()
