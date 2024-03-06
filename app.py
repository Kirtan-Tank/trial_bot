from dotenv import load_dotenv
import os
import toml
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
# from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain import HuggingFaceHub
from langchain_community.vectorstores import FAISS
from transformers import AutoTokenizer, AutoModelForCausalLM


# Caching the PDF extraction using st.cache_data
@st.cache_data
def extract_text_from_pdf(pdf):
    text = ""
    pdf_reader = PdfReader(pdf)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Caching the embeddings creation using st.cache_resource
@st.cache_resource
def create_embeddings():
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")  #sentence-transformers/all-MiniLM-L6-v2
    return embeddings

# Caching the knowledge base creation using st.cache_resource
@st.cache_resource
def create_knowledge_base(_embeddings, chunks):
    knowledge_base = FAISS.from_texts(chunks, _embeddings)
    return knowledge_base

# Caching the question answering chain loading using st.cache_resource
@st.cache_resource
def load_question_answering_chain():
    # llm = HuggingFaceHub(repo_id="Qiliang/bart-large-cnn-samsum-ChatGPT_v3", model_kwargs={"temperature": 8, "max_length": 5000, 'max_tokens': 1000})
    llm = HuggingFaceHub(repo_id="meta-llama/Llama-2-7b-chat-hf", model_kwargs={"temperature": 3, 'max_new_tokens': 1000})
    # chain = load_qa_with_sources_chain(llm, chain_type="map_reduce")
    

    chain = load_qa_chain(llm, chain_type="stuff")
    return chain

def main():
    # Load environment variables
    # load_dotenv()  # Uncomment if needed

    # Set Hugging Face Hub API token
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = st.secrets["HUGGINGFACEHUB_API_TOKEN"]

    st.set_page_config(page_title="Ask your PDF")
    st.header("Ask Your PDF")

    pdf = st.file_uploader("Upload your pdf", type="pdf")

    if pdf is not None:
        text = extract_text_from_pdf(pdf)

        # Split into chunks
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=500,
            chunk_overlap=50,
            length_function=len
        )
        chunks = text_splitter.split_text(text)

        # Create embedding
        st.write("Embeddings start")
        embeddings = create_embeddings()
        st.write("Embeddings end")

        st.write("FAISS start")
        knowledge_base = create_knowledge_base(embeddings, chunks)
        st.write("FAISS end")

        # User input
        user_question = st.text_input("Ask Question about your PDF:")

        if user_question:
            docs = knowledge_base.similarity_search(user_question, top_k=5)
            st.write("docs end")

            st.write("llm end")
            chain = load_question_answering_chain()
            st.write("chain loaded")
            st.write("Generating response...Kindly wait")
            response = chain.run(input_documents=docs, question=user_question)
            
            st.write("response ready")
            st.write(response)

if __name__ == '__main__':
    main()
