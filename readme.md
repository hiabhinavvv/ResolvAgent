ResolvAgent: An AI Support Ticket Resolution Agent

ResolvAgent is an autonomous, conversational AI agent designed to automate the triage and resolution of common customer support tickets. It features an interactive web interface built with Streamlit and leverages a powerful tool-using framework to understand user problems, retrieve information, perform actions, and communicate solutions.

This project is fully containerized with Docker to guarantee a seamless and reproducible setup on any machine, eliminating environment and dependency conflicts.

(A placeholder for a screenshot of your Streamlit app)

📝 Project Overview

In today's fast-paced digital environment, support teams are often overwhelmed with repetitive queries like password resets, billing questions, and simple configuration issues. ResolvAgent was built to tackle this challenge head-on. It acts as a first line of support, capable of handling a wide range of common tickets from start to finish.

The agent follows a "Plan-Act" loop: it parses a user's ticket, plans the steps required for resolution, uses its available tools to act on that plan, and observes the outcome to decide its next move. This allows it to either solve the problem and draft a reply or intelligently escalate the ticket to a human agent when it recognizes its limitations.

🛠️ Tech Stack

This project integrates a modern stack of AI and web development technologies:

AI & Machine Learning:

LangChain: The core framework for building the agent, managing tools, and orchestrating the LLM.

Groq: Provides the high-speed LLM (gemma2-9b-it) for the agent's reasoning and decision-making.

Sentence Transformers & FAISS: Used to create embeddings and a vector store for the RAG (Retrieval-Augmented Generation) tool, allowing the agent to search a knowledge base.

PyPDF: For parsing the PDF knowledge base.

Frontend & UI:

Streamlit: Used to build the interactive, real-time chat interface for the web application.

Backend & Infrastructure:

Python: The primary programming language for the entire application.

Docker: Used to containerize the application, ensuring a consistent and reproducible environment for deployment and submission.

Dotenv: For securely managing the API key.

🚀 How It Works: The Agent's Architecture

ResolvAgent is built on a modern Structured Tool Calling architecture. This is a reliable implementation of the conceptual "Plan-Act" loop.

Streamlit Frontend: The user interacts with the agent through the chat interface. Streamlit's session state maintains the conversational memory for each user's session.

LLM Core: The agent's reasoning is powered by Groq's qwen/qwen3-32b model. It receives the user's query and the chat history.

Tool Selection: The LLM plans its next step and, if necessary, makes a structured tool call. It has access to four distinct tools:

knowledge_base_retriever: Searches a vector database to answer questions from the IT Support Knowledge Base.pdf.

update_account_settings: A mock API to read or write user account data.

draft_reply: A mock API to format a final email response.

escalate_ticket: A mock API to log tickets that cannot be solved automatically.

Agent Executor: This LangChain runtime receives the structured tool call, executes the corresponding tool, and returns the result (the "observation") to the LLM.

Final Response: The loop continues until the agent has enough information to formulate a final answer, which is then displayed in the UI.

▶️ How to Run This Project

This project has been containerized with Docker to ensure it runs perfectly on any computer.

Prerequisites

Docker Desktop must be installed and running on your system.

Step 1: Clone the Repository

git clone https://github.com/hiabhinavvv/ResolvAgent.git
cd ResolvAgent


Step 2: Create the .env File

The application needs your Groq API key to connect to the LLM.

In the root of the project folder, create a new file named .env.

Go to GroqCloud to generate a free API key.

Add the key to your .env file. Ensure there are no extra spaces.

GROQ_API_KEY="your-secret-api-key-here"


Step 3: Build the Docker Image

This command uses the Dockerfile recipe to build a self-contained image with all dependencies and code.

docker build -t resolv-agent .


Step 4: Run the Docker Container

This command starts the application from the image you just built.

docker run -p 8501:8501 --env-file .env --name my-resolv-agent resolv-agent