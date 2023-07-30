import streamlit as st


def main():
    st.title("Home")
    st.write(
        "Welcome to Custom Chatbot where you can create a personalised chatbot by providing documents for its knowledge base!"
    )

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
