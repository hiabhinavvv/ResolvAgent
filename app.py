import streamlit as st
import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.messages import HumanMessage, AIMessage

from kb_tools import create_kb_retriever_tool
from api_tools import update_account_settings, draft_reply, escalate_ticket

@st.cache_resource
def load_agent():
    """
    Loads and initializes the LangChain agent and all its tools.
    This function is cached to ensure it only runs once.
    """
    print("--- Loading Agent and Tools for the first time... ---")
    
    load_dotenv()
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY not found in .env file")

    llm = ChatGroq(model_name="qwen/qwen3-32b", api_key=groq_api_key)

    kb_tool = create_kb_retriever_tool()
    tools = [kb_tool, update_account_settings, draft_reply, escalate_ticket]

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful and efficient AI support agent."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=5
    )

    print("--- Agent and Tools loaded successfully. ---")
    return agent_executor

def main():
    """
    The main function that runs the Streamlit UI.
    """
    st.set_page_config(page_title="ResolvAgent", page_icon="🤖")
    st.title("🤖 ResolvAgent: AI Support Chatbot")
    st.write("Welcome! I'm here to help you with your support tickets. How can I assist you today?")

    st.sidebar.title("Controls")
    if st.sidebar.button("Start New Conversation"):
        st.session_state.clear()
        st.rerun()

    agent_executor = load_agent()

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I help you resolve your support issue today?"}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Enter your support ticket here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("Thinking..."):
            chat_history = [
                HumanMessage(content=msg["content"]) if msg["role"] == "user" else AIMessage(content=msg["content"])
                for msg in st.session_state.messages
            ]

            response = agent_executor.invoke({
                "input": prompt,
                "chat_history": chat_history
            })
            
            assistant_response = response.get('output', 'Sorry, I encountered an error.')

            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            with st.chat_message("assistant"):
                st.markdown(assistant_response)

if __name__ == '__main__':
    main()