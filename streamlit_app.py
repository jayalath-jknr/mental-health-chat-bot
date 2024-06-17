# import validators, streamlit as st
# from langchain.chat_models import ChatOpenAI
# from langchain.document_loaders import UnstructuredURLLoader
# from langchain.chains.summarize import load_summarize_chain
# from langchain.prompts import PromptTemplate

# import os
# from dotenv import load_dotenv

# # Load the environment variables from the .env file
# load_dotenv()

# # Get the Cohere API key from the environment variables
# cohere_api_key = os.getenv("COHERE_API_KEY")

# import cohere

# # Streamlit app
# st.subheader('Sinhala biology Tutor')

# # Get OpenAI API key and URL to be summarized
# with st.sidebar:
#     openai_api_key = st.text_input("OpenAI API key", value="", type="password")
#     st.caption("*If you don't have an OpenAI API key, get it [here](https://platform.openai.com/account/api-keys).*")
#     model = st.selectbox("OpenAI chat model", ("gpt-3.5-turbo", "gpt-3.5-turbo-16k"))
#     # st.caption("*If the article is long, choose gpt-3.5-turbo-16k.*")
# url = st.text_input("URL", label_visibility="collapsed")

# # If 'Summarize' button is clicked
# if st.button("Answer"):
#     # Validate inputs
#     if not openai_api_key.strip() or not url.strip():
#         st.error("Please provide the missing fields.")
#     elif not validators.url(url):
#         st.error("Please enter a valid URL.")
#     else:
#         try:
#             with st.spinner("Please wait..."):
#                 # Load URL data
#                 # loader = UnstructuredURLLoader(urls=[url])
#                 # data = loader.load()
                
#                 # Initialize the ChatOpenAI module, load and run the summarize chain
#                 # Load the environment variables from the .env file
                
#                 # Get the Cohere API key from the environment variables
#                 cohere_api_key = os.getenv("COHERE_API_KEY")

#                 # Initialize the Cohere client with the API key
#                 co = cohere.Client(cohere_api_key)
# response = co.generate(
#   model='c4ai-aya',
#   prompt='ප්‍රභාසංස්ලේෂනය යනු කුමක්ද? ',
#   max_tokens=300,
#   temperature=0.9,
#   k=0,
#   stop_sequences=[],
#   return_likelihoods='NONE')
#                 # prompt = PromptTemplate(template=prompt_template, input_variables=["text"])
#                 # chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
#                 answer = .format(response.generations[0].text

#                 st.success(answer)
#         except Exception as e:
#             st.exception(f"Exception: {e}")

# # co = cohere.Client('Kt1OOYGzsH2KqnGgINooR9oZV2dbFV0qSI97mNOe') # This is your trial API key
# # response = co.generate(
# #   model='c4ai-aya',
# #   prompt='ප්‍රභාසංස්ලේෂනය යනු කුමක්ද? ',
# #   max_tokens=300,
# #   temperature=0.9,
# #   k=0,
# #   stop_sequences=[],
# #   return_likelihoods='NONE')
# # print('Prediction: {}'.format(response.generations[0].text))

# import validators, streamlit as st
# from langchain.chat_models import ChatOpenAI
# from langchain.document_loaders import UnstructuredURLLoader
# from langchain.chains.summarize import load_summarize_chain
# from langchain.prompts import PromptTemplate

# # Streamlit app
# st.subheader('Summarize URL')

# # Get OpenAI API key and URL to be summarized
# with st.sidebar:
#     openai_api_key = st.text_input("OpenAI API key", value="", type="password")
#     st.caption("*If you don't have an OpenAI API key, get it [here](https://platform.openai.com/account/api-keys).*")
#     model = st.selectbox("OpenAI chat model", ("gpt-3.5-turbo", "gpt-3.5-turbo-16k"))
#     st.caption("*If the article is long, choose gpt-3.5-turbo-16k.*")
# url = st.text_input("URL", label_visibility="collapsed")

# # If 'Summarize' button is clicked
# if st.button("Summarize"):
#     # Validate inputs
#     if not openai_api_key.strip() or not url.strip():
#         st.error("Please provide the missing fields.")
#     elif not validators.url(url):
#         st.error("Please enter a valid URL.")
#     else:
#         try:
#             with st.spinner("Please wait..."):
#                 # Load URL data
#                 loader = UnstructuredURLLoader(urls=[url])
#                 data = loader.load()
                
#                 # Initialize the ChatOpenAI module, load and run the summarize chain
#                 llm = ChatOpenAI(temperature=0, model=model, openai_api_key=openai_api_key)
#                 prompt_template = """Write a summary of the following in 250-300 words:
                    
#                     {text}

#                 """
#                 prompt = PromptTemplate(template=prompt_template, input_variables=["text"])
#                 chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
#                 summary = chain.run(data)

#                 st.success(summary)
#         except Exception as e:
#             st.exception(f"Exception: {e}")

import streamlit as st
from setup import setup  # This should only set up configurations, not load data.
from query_manager import QueryManager
from feedback_manager import FeedbackManager
from trulens_eval import Tru

def initialize_tru():
    if 'tru' not in st.session_state:
        st.session_state.tru = Tru()

def main():
    st.title('🔍 Mind Buddy')
    st.markdown("""
    Welcome to the **Mind buddy**! 🌟 This tool is designed to process your Mental health related quaries related queries with precision and provide real-time feedback. 
    """)

    initialize_tru()

    with st.sidebar:
        st.header('⚙️ Configuration')
        st.caption("Adjust system settings and initialize resources as needed.")
        if 'vector_index' not in st.session_state:
            if st.button('Initialize System', key='init_system'):
                with st.spinner('🔄 Setting up resources...'):
                    st.session_state.vector_index = setup()
                st.success('System initialized successfully! 🎉')

    st.header('📝 Submit Your Question')
    query = st.text_input('Enter your query here:', key='query_input')

    if st.button('Submit', key='submit_query'):
        if 'vector_index' not in st.session_state:
            with st.spinner('🔄 Initializing resources...'):
                st.session_state.vector_index = setup()

        query_manager = QueryManager(st.session_state.vector_index)
        st.session_state.response = query_manager.perform_query(query)

        feedback_manager = FeedbackManager(query_manager.query_engine)
        st.session_state.records = feedback_manager.record_query(query)

        # Custom HTML styling for response display
        st.markdown(f"**Response:** <div style='background-color:yellow;padding:10px;border-radius:5px;'>{st.session_state.response.response}</div>", unsafe_allow_html=True)
        st.write('Response:', st.session_state.response)
        st.write('Feedback Records:', st.session_state.records)

    manage_dashboard()

def manage_dashboard():
    st.header('🎮 Dashboard Management')
    port = 7000
    ip_address = "192.0.0.2"

    if st.button('🚀 Launch TRU Dashboard', key='launch_dashboard'):
        try:
            st.session_state.dashboard_process = st.session_state.tru.run_dashboard(port=port, force=True)
            st.success(f"🌐 Dashboard is now running on [http://{ip_address}:{port}](http://{ip_address}:{port})")
        except Exception as e:
            st.error(f"🚨 Error launching dashboard: {str(e)}")

    if st.button('🛑 Stop TRU Dashboard', key='stop_dashboard'):
        if 'dashboard_process' in st.session_state and st.session_state.dashboard_process is not None:
            st.session_state.dashboard_process.terminate()
            st.success("Dashboard has been stopped. 🛑")

if __name__ == '__main__':
    main()
