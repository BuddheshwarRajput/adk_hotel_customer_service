from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext



def get_checkin_checkout_policy(tool_context: ToolContext) -> dict:
    """
    Gets the hotel's policy on standard check-in times, check-out times,
    and procedures for late arrivals. Use this tool for any questions
    related to when a guest can arrive or must depart.
    """
    return {
        "status": "success",
        "checkin_time": "3:00 PM onwards",
        "checkout_time": "11:00 AM",
        "late_arrival_policy": (
            "Our front desk is staffed 24/7, so you can check in at any time after 3:00 PM on your arrival day. "
            "Your room is guaranteed and will be held for you. There is no need to worry about a late arrival."
        )
    }

def get_refund_policy(tool_context: ToolContext) -> dict:
    """Gets the policy for cancelling a booking and receiving a refund."""
    return {
        "status": "success",
        "policy": (
            "Guests can cancel for a full refund up to 24 hours before check-in. "
            "If canceled within 24 hours of check-in, a 1-night charge will apply. "
            "No-shows are non-refundable."
        )
    }

def get_id_policy(tool_context: ToolContext) -> dict:
    """Gets the policy on what forms of identification are required at check-in."""
    return {
        "status": "success",
        "policy": (
            "Valid government-issued ID is required at check-in. "
            "Accepted forms include Passport, Driver's License, Aadhar Card, or Voter ID."
        )
    }

def get_pets_policy(tool_context: ToolContext) -> dict:
    """Gets the policy regarding bringing pets to the hotel."""
    return {
        "status": "success",
        "policy": (
            "Pets are allowed only in designated pet-friendly rooms. "
            "A one-time cleaning fee of $50 applies. Guests must notify the front desk in advance."
        )
    }


policy_agent = Agent(
    name="policy_agent",
    model="gemini-2.0-flash",
    description="Policy agent to answer hotel policy-related questions",
    instruction="""
    You are the hotel policy agent. Your job is to help users understand our hotel’s policies clearly and professionally.

    <user_info>
    Name: {user_name}
    </user_info>

    <booking_info>
    User Bookings: {user_bookings}
    </booking_info>
    
    **REASONING INSTRUCTIONS:**
    - Your goal is to be helpful. Do not just list your tools.
    - If a user's question doesn't perfectly match a tool's name, you must INFER which tool is the most relevant.
    - **Example of Inference:** If a user asks about "arriving late" or "after midnight," you must recognize this is related to the check-in policy and use the `get_checkin_checkout_policy` tool.
    - After using a tool, formulate a helpful, natural language sentence as a response. Do not just repeat the raw output of the tool.
    
    **Your Capabilities (Tools):**
    - `get_checkin_checkout_policy`: For all questions about arrival/departure times, including late arrivals.
    - `get_refund_policy`: For questions about cancellations and refunds.
    - `get_id_policy`: For questions about required identification at check-in.
    - `get_pets_policy`: For questions about bringing pets.

    When users ask about:
    - Check-in / Check-out times → Use get_checkin_checkout_policy
    - Refunds or cancellation → Use get_refund_policy
    - ID proof requirements → Use get_id_policy
    - Pet policy → Use get_pets_policy

    Example Questions:
    - "When is check-in and check-out?"
    - "Can I cancel my booking and get a refund?"
    - "What ID do I need to carry?"
    - "Are pets allowed?"

    Be factual, polite, and clear. Avoid uncertainty or vague answers.
    """,
    tools=[
        get_checkin_checkout_policy,
        get_refund_policy,
        get_id_policy,
        get_pets_policy
    ],
)
