HFModelPlayGround: Customizable Hugging Face Model Testing Platform

This project is a Streamlit application designed to enable users to test Hugging Face large language models (LLMs) with customizable parameters, such as embedding models and LLM configurations. Users can upload PDF documents, ask questions about their content, and experiment with different Hugging Face models and settings.

Features

PDF Text Extraction:

Upload a PDF, and the app extracts text from all its pages.

Customizable Model Parameters:

Specify the Hugging Face LLM and embedding model via user inputs.

Test different configurations like temperature and token limits for LLMs.

Text Chunking:

Splits the extracted text into manageable chunks to optimize embedding generation and question answering.

Embeddings and Vector Store:

Uses Hugging Face embeddings to represent text semantically.

Stores the embeddings in a FAISS (Facebook AI Similarity Search) vector store for efficient similarity search.

LLM Integration:

Supports integration with Hugging Face LLMs, allowing quick experimentation.

Question Answering:

Retrieves the most relevant text chunks and generates a response using the specified LLM.

Installation

Prerequisites

Ensure you have the following installed:

Python 3.8 or higher

Pip package manager

Hugging Face API token (create one at Hugging Face)

Steps

Clone the repository:

git clone https://github.com/your-repo/ask-your-pdf.git
cd ask-your-pdf

Install dependencies:

pip install -r requirements.txt

Set up environment variables:

Create a .streamlit/secrets.toml file in the root directory.

Add your Hugging Face API token:

[secrets]
HUGGINGFACEHUB_API_TOKEN = "your_api_token_here"

Usage

Run the Streamlit app:

streamlit run app.py

Open the app in your browser (usually at http://localhost:8501).

Upload a PDF and configure the following parameters:

Hugging Face LLM repository ID (e.g., bigscience/bloom-560m).

Hugging Face Embedding model repository ID (e.g., BAAI/bge-small-en-v1.5).

Enter a question about the PDF content. The app will:

Extract text from the PDF.

Generate embeddings for text chunks.

Perform similarity search to retrieve relevant chunks.

Use the specified Hugging Face LLM to answer your question.

Key Libraries and Tools

Streamlit: For creating the user interface.

PyPDF2: For extracting text from PDF documents.

LangChain: For building the question-answering pipeline.

Hugging Face Hub: For accessing state-of-the-art LLMs and embedding models.

FAISS: For efficient similarity search on embeddings.

Transformers: For loading Hugging Face models.

Key Functions

extract_text_from_pdf:
Extracts text from the uploaded PDF using PyPDF2 and caches the result.

create_embeddings:
Generates text embeddings using Hugging Face embedding models. Allows customization of the embedding model via user input.

create_knowledge_base:
Builds a FAISS knowledge base for similarity search, storing text chunks and their embeddings.

load_question_answering_chain:
Initializes the question-answering chain with a customizable Hugging Face LLM and settings like temperature and max_new_tokens.

Customization

Change the LLM and embedding model dynamically by providing the desired repository IDs in the app interface.

Adjust LLM parameters like temperature and max_new_tokens via the load_question_answering_chain function.

Modify text chunking parameters (e.g., chunk_size, chunk_overlap) in the CharacterTextSplitter initialization.

Notes

This project is designed for quick testing and experimentation with Hugging Face models.

Ensure your Hugging Face API token has the necessary permissions to access the desired models.

Some models may require significant compute resources.

Future Enhancements

Add support for more complex chain types (e.g., map-reduce).

Extend functionality to handle multi-modal input (e.g., images or tables).

Incorporate additional vector stores or database integrations.

Improve caching for faster repeat queries.

Contributing

If you'd like to contribute, feel free to fork the repository and submit a pull request. Bug reports and feature requests are welcome!

License

This project is licensed under the MIT License. See the LICENSE file for details.

Author

Kirtan Tank

Email: cosmickirtan@gmail.com

Copyright

© 2025 Kirtan Tank. All rights reserved. Unauthorized copying, modification, or distribution of this software is prohibited without prior permission from the copyright holder.

