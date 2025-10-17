import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

vector_store = None

mock_user_database = {
    "user_001": {"name": "Alice", "plan": "Free Tier", "invoices": ["inv_123", "inv_456"]},
    "user_002": {"name": "Bob", "plan": "Pro Monthly", "invoices": ["inv_789"]},
    "user_003": {"name": "Charlie", "plan": "Pro Annual", "invoices": []},
}


def setup_knowledge_base():
    global vector_store
    print("Setting up the Knowledge Base...")
    if not os.path.exists('docs'):
        print("The 'docs' folder was not found. Please create it and add your PDF files.")
        return

    loader = PyPDFDirectoryLoader("docs/")
    documents = loader.load()

    if not documents:
        print("No documents found in the 'docs' folder. The knowledge base will be empty.")
        return
        
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=750, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)
    
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    vector_store = FAISS.from_documents(docs, embeddings)
    print("--- Knowledge Base setup complete! ---")



def knowledge_base_retriever(query: str) -> str:
    global vector_store
    print(f"--- TOOL: Querying Knowledge Base for: '{query}' ---")
    if vector_store is None:
        return "Error: The knowledge base is not set up. Please run the setup function."
        
    results = vector_store.similarity_search(query, k=1)
    
    if not results:
        return "No relevant information found in the knowledge base."
        
    context = "\n\n".join([doc.page_content for doc in results])
    return f"Found the following information:\n---\n{context}\n---"


def get_user_config(user_id: str) -> dict:
    print(f"TOOL: Checking config for user: {user_id}")
    if user_id in mock_user_database:
        return mock_user_database[user_id]
    else:
        return {"error": "User not found."}


def draft_reply_email(recipient_name: str, message_body: str) -> dict:
    print(f"TOOL: Drafting email to {recipient_name}")
    email_draft = f"""
    --------------------
    To: {recipient_name}
    Subject: Regarding your recent support ticket

    Hello {recipient_name},

    {message_body}

    Best regards,
    The Support Team
    --------------------
    """
    print(email_draft)
    return {"status": "success", "draft": email_draft}


def escalate_to_human(ticket_id: str, summary: str, reason: str) -> dict:
    print(f"--- TOOL: ESCALATING TICKET {ticket_id} TO HUMAN ---")
    escalation_note = f"""
    --------------------
    ESCALATION
    Ticket ID: {ticket_id}
    Reason: {reason}
    Summary: {summary}
    --------------------
    """
    print(escalation_note)
    return {"status": "escalated", "note": escalation_note}

if __name__ == '__main__':
    setup_knowledge_base()
    if vector_store:
        test_query = "how do i reset my password"
        print(f"\n--- Testing the Knowledge Base with query: '{test_query}' ---")
        retrieved_info = knowledge_base_retriever(query=test_query)
        print(retrieved_info)