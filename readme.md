ResolvAgent: An AI Support Ticket Resolution Agent

ResolvAgent is an autonomous, conversational AI agent designed to automate the triage and resolution of common customer support tickets. It leverages the power of Large Language Models (LLMs) and a tool-using framework to understand user problems, retrieve information, perform actions, and communicate solutions, significantly reducing the workload on human support teams.

This project was built using LangChain, with Groq providing the high-speed LLM inference.

✨ Features

Natural Language Understanding: Parses and understands support tickets written in plain English.

Tool-Using Capability: Utilizes a suite of tools to perform specific actions like retrieving data, updating accounts, or drafting replies.

Knowledge Base Integration (RAG): Answers questions by searching and synthesizing information from a provided PDF knowledge base.

Mock Account Management: Simulates reading and writing user data (e.g., checking or upgrading a subscription plan) via a mock API.

Automated Communication: Intelligently drafts formatted email replies to users once a solution is found.

Intelligent Escalation: Recognizes when it cannot solve a ticket and automatically escalates the issue with a summary for a human agent.

Conversational Memory: Remembers the context of the ongoing conversation to handle multi-turn queries effectively.

🚀 How It Works (Architecture)

ResolvAgent is built on a modern Structured Tool Calling agent architecture. This model follows a conceptual "Plan-Act" loop, where the agent reasons about the user's request, selects the appropriate tool, and continues this cycle until the ticket is resolved.

LLM Core: The agent's reasoning is powered by Groq's gemma2-9b-it model, which excels at understanding instructions and making decisions about tool usage.

Tools: The agent has access to four distinct tools:

knowledge_base_retriever: Searches a FAISS vector index built from the IT Support Knowledge Base.pdf to answer factual questions.

update_account_settings: A mock API to read or write user data from a simulated database.

draft_reply: A mock API to format and prepare a final email response to the user.

escalate_ticket: A mock API to log tickets that cannot be solved automatically, flagging them for human review.

Agent Executor: This is the runtime provided by LangChain that orchestrates the entire process. It passes the user's request to the agent, executes the tool calls the agent decides on, and feeds the results back to the agent to inform its next step.

📂 Project Structure

ResolvAgent/
├── .venv/                  # Virtual environment
├── docs/
│   └── IT Support Knowledge Base.pdf  # The agent's knowledge source
├── .env                    # For storing API keys (ignored by Git)
├── .gitignore              # Specifies files for Git to ignore
├── api_tools.py            # Defines the mock API tools
├── kb_tools.py             # Defines the knowledge base (RAG) tool
├── requirements.txt        # Project dependencies
└── run_agent.py            # Main script to run the agent


⚙️ Setup and Installation

Follow these steps to run ResolvAgent on your local machine.

1. Clone the Repository

git clone [https://github.com/hiabhinavvv/ResolvAgent.git](https://github.com/hiabhinavvv/ResolvAgent.git)
cd ResolvAgent


2. Set Up a Python Virtual Environment

This keeps your project dependencies isolated.

# For macOS/Linux
python3 -m venv .venv
source .venv/bin/activate

# For Windows
python -m venv .venv
.\.venv\Scripts\activate


3. Install Dependencies

Install all the required Python packages from the requirements.txt file.

pip install -r requirements.txt


4. Configure Environment Variables

The agent needs a Groq API key to function.

Create a file named .env in the root of the project directory.

Go to GroqCloud to get your free API key.

Add the key to your .env file like this:

GROQ_API_KEY="your-secret-api-key-here"


The .gitignore file is already configured to prevent this file from being committed.

5. Place the Knowledge Base

Make sure your IT Support Knowledge Base.pdf file is placed inside the docs/ folder.

▶️ How to Run the Agent

Once the setup is complete, you can start the agent with a single command:

python run_agent.py