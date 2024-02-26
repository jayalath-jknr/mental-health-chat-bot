import validators, streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import UnstructuredURLLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate

import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

# Get the Cohere API key from the environment variables
cohere_api_key = os.getenv("COHERE_API_KEY")

import cohere

# Streamlit app
st.subheader('Sinhala biology Tutor')

# Get OpenAI API key and URL to be summarized
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API key", value="", type="password")
    st.caption("*If you don't have an OpenAI API key, get it [here](https://platform.openai.com/account/api-keys).*")
    model = st.selectbox("OpenAI chat model", ("gpt-3.5-turbo", "gpt-3.5-turbo-16k"))
    # st.caption("*If the article is long, choose gpt-3.5-turbo-16k.*")
url = st.text_input("URL", label_visibility="collapsed")

# If 'Summarize' button is clicked
if st.button("Answer"):
    # Validate inputs
    if not openai_api_key.strip() or not url.strip():
        st.error("Please provide the missing fields.")
    elif not validators.url(url):
        st.error("Please enter a valid URL.")
    else:
        try:
            with st.spinner("Please wait..."):
                # Load URL data
                # loader = UnstructuredURLLoader(urls=[url])
                # data = loader.load()
                
                # Initialize the ChatOpenAI module, load and run the summarize chain
                # Load the environment variables from the .env file
                
                # Get the Cohere API key from the environment variables
                cohere_api_key = os.getenv("COHERE_API_KEY")

                # Initialize the Cohere client with the API key
                co = cohere.Client(cohere_api_key)
response = co.generate(
  model='c4ai-aya',
  prompt='ප්‍රභාසංස්ලේෂනය යනු කුමක්ද? ',
  max_tokens=300,
  temperature=0.9,
  k=0,
  stop_sequences=[],
  return_likelihoods='NONE')
                # prompt = PromptTemplate(template=prompt_template, input_variables=["text"])
                # chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
                answer = .format(response.generations[0].text

                st.success(answer)
        except Exception as e:
            st.exception(f"Exception: {e}")

# co = cohere.Client('Kt1OOYGzsH2KqnGgINooR9oZV2dbFV0qSI97mNOe') # This is your trial API key
# response = co.generate(
#   model='c4ai-aya',
#   prompt='ප්‍රභාසංස්ලේෂනය යනු කුමක්ද? ',
#   max_tokens=300,
#   temperature=0.9,
#   k=0,
#   stop_sequences=[],
#   return_likelihoods='NONE')
# print('Prediction: {}'.format(response.generations[0].text))