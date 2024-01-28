from dotenv import load_dotenv
import os
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain import HuggingFaceHub

def main():
    #load_dotenv()
    os.environ["HUGGINGFACEHUB_API_TOKEN"]=st.secrets["HUGGINGFACEHUB_API_TOKEN"]
    st.set_page_config(page_title="Ask your PDF")
    st.header("Ask Your PDF")

    pdf = st.file_uploader("Upload your pdf", type="pdf")

    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        # Split into chunks
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text)

        # Create embedding
        st.write("Embeddings start")
        embeddings = HuggingFaceEmbeddings(model_name ="sentence-transformers/all-MiniLM-L6-v2")
        st.write("Embeddings end")
        st.write("FAISS start")
        knowledge_base = FAISS.from_texts(chunks, embeddings)
        st.write("FAISS end")    
        # User input
        user_question = st.text_input("Ask Question about your PDF:")

        if user_question:
            docs = knowledge_base.similarity_search(user_question)
            st.write("docs end")
            llm = HuggingFaceHub(repo_id="tiiuae/falcon-40b-instruct", model_kwargs={"temperature":2})
            st.write("llm end")
            chain = load_qa_chain(llm, chain_type="stuff")
            st.write("chain loaded")
            response = chain.run(input_documents=docs, question=user_question)
            st.write("response ready")
            st.write(response)

if __name__ == '__main__':
    main()
