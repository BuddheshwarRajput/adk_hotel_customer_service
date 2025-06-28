from google.adk.agents import Agent
from datetime import datetime
from google.adk.tools.tool_context import ToolContext




def get_room_upgrade_options(tool_context: ToolContext, current_room: str) -> dict:
    # current_room = tool_context._invocation_context.tool_arguments.get("current_room", "").strip()

    upgrades = {
        "Standard Room": ["Deluxe Room", "Executive Suite"],
        "Deluxe Room": ["Executive Suite", "Penthouse Suite"],
        "Family Room": ["Executive Suite", "Penthouse Suite"],
        "Executive Suite": ["Penthouse Suite"],
        "Penthouse Suite": []
    }

    if not current_room:
        return {"status": "error", "message": "Current room not specified."}

    options = upgrades.get(current_room)
    if options is None:
        return {"status": "error", "message": f"Unknown room type: {current_room}"}

    return {
        "status": "success",
        "available_upgrades": options or ["No upgrades available."]
    }


def check_user_booking(tool_context: ToolContext) -> dict:
    user_bookings = tool_context.state.get("user_bookings", [])

    if not user_bookings:
        return {"status": "info", "message": "No active or upcoming bookings found."}

    active = [
        f"Room ID: {b['room_id']}, Check-in: {b['check_in']}, Check-out: {b['check_out']}"
        for b in user_bookings if isinstance(b, dict)
    ]

    return {
        "status": "success",
        "bookings": active
    }


def check_room_features(tool_context: ToolContext, room_type: str) -> dict:
    # room_type = tool_context._invocation_context.tool_arguments.get("room_type", "").strip()

    features = {
        "Deluxe Room": "King-size bed, city view, complimentary breakfast.",
        "Executive Suite": "Living area, minibar, lounge access.",
        "Family Room": "Two queen beds, kid-friendly amenities, extra space.",
        "Standard Room": "Budget-friendly, basic amenities, compact space.",
        "Penthouse Suite": "Panoramic views, private balcony, hot tub, luxury furnishings."
    }

    if not room_type:
        return {"status": "error", "message": "Room type not provided."}

    feature = features.get(room_type)
    if not feature:
        return {"status": "error", "message": f"Unknown room type: {room_type}"}

    return {
        "status": "success",
        "room_type": room_type,
        "features": feature
    }

def report_room_issue(tool_context: ToolContext, room_id: str, issue_description: str) -> dict:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not room_id or not issue_description:
        return {"status": "error", "message": "Room ID and issue description are required."}


    issues = tool_context.state.get("reported_issues", [])
    issues.append({
        "room_id": room_id,
        "description": issue_description,
        "timestamp": timestamp
    })
    tool_context.state["reported_issues"] = issues

    return {
        "status": "success",
        "message": f"Issue reported for Room {room_id}: {issue_description}. Support will address it shortly.",
        "timestamp": timestamp
    }



room_support_agent = Agent(
    name="room_support_agent",
    model="gemini-2.0-flash",
    description="Room support agent for hotel booking assistance",
    instruction="""
    You are the room support agent for a hotel booking system.
    Your role is to help users with questions about room types, features, and availability.

    <user_info>
    Name: {user_name}
    </user_info>

    <booking_info>
    Current Bookings: {user_bookings}
    </booking_info>

    Before helping:
    - Check if the user has a booking with this hotel
    - Bookings are stored as objects with "room_id", "check_in", and "check_out" properties
    - Only provide specific room support if they have an active or upcoming booking
    - If no booking exists, redirect them to the booking agent
    - If a booking exists, you can reference their room type and dates

    Room Types:
    1. Deluxe Room
       - King-size bed
       - City view
       - Complimentary breakfast

    2. Executive Suite
       - Separate living area
       - Workspace and minibar
       - Access to executive lounge

    3. Family Room
       - Two queen beds
       - Kid-friendly amenities
       - Extra space for luggage

    4. Standard Room
       - Budget-friendly
       - Basic amenities
       - Compact space

    5. Penthouse Suite
       - Top-floor panoramic views
       - Private balcony and hot tub
       - Premium furnishings and décor

    When helping:
    1. Recommend room types based on needs (e.g., family, work, luxury)
    2. Explain features clearly and compare room options
    3. Confirm booking details if applicable
    4. Encourage contacting the booking agent for room upgrades or changes
    """,
    tools=[
        check_room_features,
        check_user_booking,
        get_room_upgrade_options,
        report_room_issue
        ],
)
