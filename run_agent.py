import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor

from langchain_core.messages import HumanMessage, AIMessage

from kb_tools import create_kb_retriever_tool
from api_tools import update_account_settings, draft_reply, escalate_ticket

def main():
    """
    This function sets up and runs the AI Support Agent using the modern
    Structured Tool Calling approach.
    """
    load_dotenv()
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY not found in .env file")

    llm = ChatGroq(model_name="qwen/qwen3-32b", api_key=groq_api_key)

    print("Initializing tools...")
    kb_tool = create_kb_retriever_tool()
    
    tools = [
        kb_tool,
        update_account_settings,
        draft_reply,
        escalate_ticket
    ]
    print("Tools initialized successfully.")

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful and efficient AI support agent. You have a memory of the conversation."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_tool_calling_agent(
        llm=llm,
        tools=tools,
        prompt=prompt,
    )

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True, 
        max_iterations=5 
    )

    print("\n--- AI Support Agent is Ready ---")
    print("Enter a support ticket to begin. Type '/clear' for a new conversation, or '/exit' to quit.")
    chat_history = []

    while True:
        user_input = input("\nSupport Ticket: ")
        if user_input.lower() == '/exit':
            break

        if user_input.lower() == '/clear':
            chat_history = []
            print("\n--- New conversation started. Agent's memory has been cleared. ---")
            continue
        
        try:
            response = agent_executor.invoke({
                "input": user_input,
                "chat_history": chat_history
            })

            chat_history.append(HumanMessage(content=user_input))
            chat_history.append(AIMessage(content=response['output']))

            print("\n--- Agent's Final Response ---")
            print(response['output'])
        except Exception as e:
            print(f"\nAn error occurred: {e}")

if __name__ == '__main__':
    main()