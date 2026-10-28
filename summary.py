import streamlit as st
from llm_res import llm
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import WebBaseLoader

def summary(link):
 loader = WebBaseLoader(link)
 data = loader.load().pop().page_content
 prompt_extract = PromptTemplate.from_template(
    """
    ### SCRAPED TEXT FROM WEBSITE:
    {data}
    ### INSTRUCTIONS:
    The scraped text is from the langchain wekipidea
    Your job is to tell the summary of that data in simple words in 5 to 10 lines.
    """
)

 chain_extract = prompt_extract | llm | StrOutputParser()
 res = chain_extract.invoke({"data": data})
 st.write("\n### SUMMARY ###")
 st.write(res)
 

st.title("Get Summary")
link = st.text_input("Enter the link")

if st.button("Get Summary"):
  summary(link)