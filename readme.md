<div align="center">

ResolvAgent: AI Support Ticket Resolution Agent

An autonomous, containerized AI agent that understands, resolves, and escalates support tickets.

</div>

<!-- Optional: Add a screenshot of your app here -->

<!-- <p align="center">
<img src="PATH_TO_YOUR_SCREENSHOT.png" alt="ResolvAgent Screenshot" width="700">
</p> -->

📝 Project Overview

ResolvAgent is a full-stack, conversational AI application designed to automate the triage and resolution of common customer support tickets. It acts as an intelligent first line of support, capable of handling repetitive queries like password resets, billing questions, and plan upgrades.

The agent follows a "Plan-Act" loop: it parses a user's ticket, plans the steps required, uses its available tools to act on that plan, and observes the outcome to decide its next move. This allows it to either solve the problem and draft a reply or intelligently escalate the ticket to a human agent when it recognizes its limitations.

✨ Key Features

🤖 Autonomous Agent: Follows a "Plan-Act" loop to reason and resolve tickets from start to finish.

🛠️ Structured Tool-Using: Intelligently selects from a suite of tools (RAG, Account APIs, Email Drafts) to perform real-world actions.

🖥️ Interactive Web UI: A real-time, conversational chat interface built with Streamlit.

🧠 RAG-Powered Knowledge: Uses a FAISS vector store (from a PDF knowledge base) to retrieve and reason about information.

🐳 Fully Containerized: Guaranteed one-command setup using Docker, eliminating all "it works on my machine" problems.

💭 Conversational Memory: Remembers the context of the ongoing conversation to handle multi-turn queries.

🛠️ How It Works: The Agent's Architecture

ResolvAgent is built on a modern Structured Tool Calling architecture. This is a highly reliable implementation of the conceptual "Plan-Act" loop.

Streamlit Frontend: The user interacts with the agent via the chat interface. Streamlit's session_state maintains the conversational memory for each user.

LLM Core: The agent's reasoning is powered by Groq's qwen/qwen3-32b model. It receives the user's query and the chat history.

Tool Selection: The LLM plans its next step and makes a structured tool call. It has access to four distinct tools:

knowledge_base_retriever: Searches a vector database to answer questions from the IT Support Knowledge Base.pdf.

update_account_settings: A mock API to read or write user account data.

draft_reply: A mock API to format a final email response.

escalate_ticket: A mock API to log tickets that cannot be solved automatically.

Agent Executor: This LangChain runtime receives the structured tool call, executes the corresponding tool, and returns the result (the "observation") back to the LLM.

Final Response: The loop continues until the agent has enough information to formulate a final answer, which is then displayed in the UI.

💻 Tech Stack

LangChain

Core framework for building the agent and managing tools.

LLM Inference

Groq

Provides the high-speed qwen/qwen3-32b model for reasoning.

Frontend

Streamlit

Building the interactive web UI.

Containerization

Docker

Creating a reproducible, isolated environment.

RAG Backend

FAISS & Sentence-Transformers

Vector store and text embeddings for RAG.

PDF Parsing

PyPDF

Extracting text from the knowledge base document.

▶️ How to Run This Project

This project is fully containerized with Docker to ensure it runs perfectly on any computer.

Prerequisites

Docker Desktop must be installed and running on your system.

You must have a Groq API key. Get one for free at GroqCloud.

Option 1: The Bulletproof Way (Recommended)

This method uses a pre-built Docker image and does not require a stable internet connection to build. It is the fastest and most reliable way to run the application, as it bypasses any potential network or firewall issues.

1. Get the Project Files

git clone [https://github.com/hiabhinavvv/ResolvAgent.git](https://github.com/hiabhinavvv/ResolvAgent.git)
cd ResolvAgent


2. Download the Pre-Built Image
Download the resolv-agent-image.tar file (approx. 5GB) from the following link:

➡️ https://drive.google.com/file/d/1mXr4bBEMQKHTRAsv3pSnK8lkPocWD-2u/view?usp=sharing

Place this .tar file in the ResolvAgent project directory you just cloned.

3. Load the Image into Docker
This command loads the pre-built application into your local Docker.

docker load -i resolv-agent-image.tar


4. Create Your .env File
Create a new file named .env in the project directory and add your Groq API key.

GROQ_API_KEY="your-secret-api-key-here"


5. Run the Container
This command starts the application.

docker run -p 8501:8501 --env-file .env --name my-resolv-agent resolv-agent


6. Access the Application
Open your web browser and navigate to: http://localhost:8501

Option 2: Build from Source (Alternative)

Use this method only if you have a stable, unrestricted internet connection and want to build the image from the Dockerfile yourself.

(Note: This build process may fail if you are on a network with a restrictive firewall, such as some corporate or university networks, that blocks downloads from Docker Hub.)

1. Clone the Project

git clone [https://github.com/hiabhinavvv/ResolvAgent.git](https://github.com/hiabhinavvv/ResolvAgent.git)
cd ResolvAgent


2. Create Your .env File
Create a file named .env and add your Groq API key.

GROQ_API_KEY="your-secret-api-key-here"


3. Build the Docker Image
This command will download the Python base image and install all dependencies.

docker build -t resolv-agent .


4. Run the Container

docker run -p 8501:8501 --env-file .env --name my-resolv-agent resolv-agent


5. Access the Application
Open your web browser and navigate to: http://localhost:8501