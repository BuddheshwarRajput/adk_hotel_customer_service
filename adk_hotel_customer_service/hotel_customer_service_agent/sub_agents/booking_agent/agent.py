import os


from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
from datetime import datetime


def get_booking_history(tool_context: ToolContext) -> dict:
    bookings = tool_context.state.get("user_bookings", [])
    if not bookings:
        return {"status": "info", "message": "No bookings found."}
    
    formatted = [
        f"{b.get('room_type', 'Room')} | Check-in: {b.get('check_in')} | Check-out: {b.get('check_out')}"
        for b in bookings if isinstance(b, dict)
    ]
    return {"status": "success", "message": "Your booking history:", "bookings": formatted}


def refund_booking(tool_context: ToolContext, room_id: str) -> dict:
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    bookings = tool_context.state.get("user_bookings", [])
    remaining = []
    refunded = False
    for booking in bookings:
        if isinstance(booking, dict) and booking.get("room_id") == room_id:
            refunded = True
            continue
        remaining.append(booking)
    if not refunded:
        return {"status": "error", "message": f"No booking found with Room ID: {room_id}"}
    tool_context.state["user_bookings"] = remaining
    tool_context.state.setdefault("interaction_history", []).append({
        "action": "refund_booking", "room_id": room_id, "timestamp": current_time
    })
    return {"status": "success", "message": f"Booking for Room ID {room_id} refunded.", "timestamp": current_time}


def cancel_booking(tool_context: ToolContext, room_id: str, check_in: str) -> dict:
    bookings = tool_context.state.get("user_bookings", [])
    remaining = []
    canceled = False
    for booking in bookings:
        if (booking.get("room_id") == room_id and booking.get("check_in") == check_in):
            canceled = True
            continue
        remaining.append(booking)
    if not canceled:
        return {"status": "error", "message": "No matching booking found to cancel."}
    tool_context.state["user_bookings"] = remaining
    return {"status": "success", "message": f"Booking for Room ID {room_id} starting on {check_in} canceled."}

booking_agent = Agent(
    name="booking_agent",

    model="gemini-1.5-flash",
    description="Booking agent for hotel reservation management",
    instruction="""
    You are the booking agent for the hotel's reservation system.
    Your primary role is to help users view their bookings and process cancellations or refunds.

    **CRITICAL LOGIC FOR HANDLING CANCELLATIONS/REFUNDS:**
    When a user asks to cancel or refund a booking, you MUST follow this sequence:

    1.  **ALWAYS check for existing bookings first.** Use the `get_booking_history` tool immediately to see what reservations the user has.

    2.  **Analyze the result of `get_booking_history`:**
        - **If the tool returns "No bookings found":** Your job is to inform the user they have no active bookings to cancel. Do NOT ask for more information. A good response would be: "It looks like you don't have any bookings with us right now. Can I help with anything else?"
        - **If the tool returns ONE booking:** The user probably means this one. Confirm with them before taking action. Ask a clarifying question like: "I see you have one booking for the [Room Type] checking in on [Date]. Is this the one you'd like to cancel?"
        - **If the tool returns MORE THAN ONE booking:** You must ask the user to specify which one. Say something like: "You have multiple bookings with us. Please provide the Room ID and check-in date for the reservation you wish to cancel."

    3.  **Only when you have confirmed the correct `room_id` and `check_in` date**, you may then use the `cancel_booking` or `refund_booking` tools to complete the action.

    DO NOT attempt to call `cancel_booking` or `refund_booking` without first verifying the user's bookings and getting all required information.
    """,
    tools=[refund_booking, cancel_booking, get_booking_history],
)








