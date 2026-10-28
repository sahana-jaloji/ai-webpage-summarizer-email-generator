import streamlit as st
from llm_res import llm
from langchain_community.document_loaders import WebBaseLoader
from prompt import prompt_extract,prompt_email
from langchain_core.output_parsers import JsonOutputParser
import pandas as pd
import uuid
import chromadb

st.header("Email Generator")
link = st.text_input("Enter the job link")

if st.button("Generate Email"):
    loader = WebBaseLoader(link)
    data = loader.load().pop().page_content

    chain_extract = prompt_extract | llm
    res = chain_extract.invoke(input={"data":data})
    # print(res.content)

    json_parser = JsonOutputParser()
    json_res = json_parser.parse(res.content)
    job = json_res[0] if isinstance(json_res, list) else json_res

    df = pd.read_csv("my_portfolio.csv")

    client = chromadb.PersistentClient('vectorstore')
    new_collection = client.get_or_create_collection(name="portfolio")

    if not new_collection.count():
        for _, row in df.iterrows():
            new_collection.add(
            documents=row["Techstack"],
            metadatas={"links":row["Links"]},
            ids=[str(uuid.uuid4())]
        )
    links = new_collection.query(query_texts=job['skills'], n_results=2).get('metadatas', [])

    chain_email = prompt_email | llm
    final_res = chain_email.invoke({"job_description":str(job), "link_list":links})
    st.write(final_res.content)


            



       
        
    




