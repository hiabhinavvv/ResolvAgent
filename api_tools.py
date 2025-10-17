from langchain.tools import tool
from typing import Optional

mock_user_database = {
    "user123": {"name": "Alice", "subscription_plan": "Basic"},
    "user456": {"name": "Bob", "subscription_plan": "Pro"},
}

@tool
def update_account_settings(user_id: str, action: str, new_plan: Optional[str] = None) -> str:
    """
    Use to read or update account settings, like subscription plans.
    Requires 'user_id' and 'action' ('read'/'write').
    If action is 'write', also provide 'new_plan'.
    """
    global mock_user_database
    print(f"\n> Calling Account Settings API with: user_id={user_id}, action={action}, new_plan={new_plan}")
    
    if user_id not in mock_user_database:
        return f"Error: User with ID '{user_id}' not found."

    if action.lower() == 'read':
        plan = mock_user_database[user_id]['subscription_plan']
        return f"Success: User '{user_id}' is on the '{plan}' plan."

    elif action.lower() == 'write':
        if not new_plan:
            return "Error: 'new_plan' is required for a 'write' action."
        
        valid_plans = ["Basic", "Pro", "Enterprise"]
        if new_plan not in valid_plans:
            return f"Error: Invalid plan '{new_plan}'. Must be one of {valid_plans}."

        mock_user_database[user_id]['subscription_plan'] = new_plan
        return f"Success: User '{user_id}' plan updated to '{new_plan}'."

    else:
        return "Error: Invalid action. Must be 'read' or 'write'."

@tool
def draft_reply(recipient_email: str, message_body: str) -> str:
    """Use to draft an email reply to a customer after resolving an issue."""
    print(f"\n> Calling Email API: Drafting reply to {recipient_email}")
    email_content = f"--- EMAIL DRAFT ---\nTO: {recipient_email}\nSUBJECT: Support Ticket Update\n\nBODY:\n{message_body}\n--- END OF DRAFT ---"
    print(email_content)
    return "Success: The reply has been drafted."

@tool
def escalate_ticket(summary: str) -> str:
    """
    Use ONLY when an issue cannot be resolved by other tools.
    This hands the ticket to a human. Input must be a clear summary of the problem.
    """
    print(f"\n> Calling Escalation Logger API")
    log_entry = f"--- TICKET ESCALATION ---\nSTATUS: Needs Human Review\nSUMMARY: {summary}\n--- END OF LOG ---"
    print(log_entry)
    return "Success: Ticket escalated for human review."

if __name__ == '__main__':
    print("--- Testing Mock API Tools (using simple dictionary) ---")

    # Test 1: Read account settings
    read_result = update_account_settings.invoke({"user_id": "user123", "action": "read"})
    print(f"Tool Output: {read_result}\n")

    # Test 2: Update account settings
    write_result = update_account_settings.invoke({"user_id": "user456", "action": "write", "new_plan": "Enterprise"})
    print(f"Tool Output: {write_result}")
    read_after_write = update_account_settings.invoke({"user_id": "user456", "action": "read"})
    print(f"Tool Output: {read_after_write}\n")

    # Test 3: Draft an email
    email_result = draft_reply.invoke({
        "recipient_email": "customer@example.com",
        "message_body": "Your password has been successfully reset."
    })
    print(f"Tool Output: {email_result}\n")
    
    # Test 4: Escalate a ticket
    escalation_result = escalate_ticket.invoke(
        {"summary": "User is missing an invoice for August. No solution in KB, and account API does not support invoice management."}
    )
    print(f"Tool Output: {escalation_result}\n")