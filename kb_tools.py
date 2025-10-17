import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from langchain.tools import tool

load_dotenv()

def create_kb_retriever_tool():
    """
    This function creates the RAG pipeline and returns a tool-decorated function
    that consistently accepts a dictionary input.
    """
    print("Building the Knowledge Base Retriever Tool...")

    loader = PyPDFLoader("docs/IT Support Knowledge Base.pdf")
    documents = loader.load()
    print(f"Loaded {len(documents)} pages from the PDF.")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=750, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)
    print(f"Split the document into {len(docs)} chunks.")

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    db = FAISS.from_documents(docs, embeddings)

    retriever = db.as_retriever(search_kwargs={'k': 1})
    print("FAISS vector store and retriever created.")
    @tool
    def knowledge_base_retriever(query: str) -> str:
        """
        Use this tool to find information and answer questions about IT support topics.
        It is the primary source for topics like password resets, billing issues,
        subscription plans, technical troubleshooting, and account management.
        The input MUST be a dictionary with a single key 'query' and the search term as the value.
        """
        retrieved_docs = retriever.invoke(query)
        return "\n\n".join(doc.page_content for doc in retrieved_docs)

    print("Knowledge Base Retriever Tool created successfully.")
    return knowledge_base_retriever

if __name__ == '__main__':
    kb_tool = create_kb_retriever_tool()

    query = "How do I reset my password?"
    results = kb_tool.invoke(query)

    print(f"\n--- Test Query: '{query}' ---")
    for doc in results:
        print(f"Content: {doc.page_content}\n")