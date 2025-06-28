from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
import sys 

def list_available_rooms(tool_context: ToolContext) -> dict:
    rooms = [
        "Standard Room - Compact, budget-friendly",
        "Deluxe Room - King bed, city view, breakfast included",
        "Executive Suite - Lounge access, minibar, workspace",
        "Family Room - Two queen beds, kid-friendly features",
        "Penthouse Suite - Private balcony, hot tub, luxury view"
    ]
    return {
        "status": "success",
        "available_rooms": rooms
    }

def get_room_price(tool_context: ToolContext, room_type: str) -> dict:

    prices = {
        "Standard Room": "$89 per night",
        "Deluxe Room": "$129 per night",
        "Executive Suite": "$199 per night",
        "Family Room": "$159 per night",
        "Penthouse Suite": "$299 per night"
    }

    if not room_type or room_type not in prices:
        return {
            "status": "error",
            "message": "Room type not recognized. Please ask for pricing using a valid room name."
        }

    return {
        "status": "success",
        "room_type": room_type,
        "price": prices[room_type]
    }

def offer_deals(tool_context: ToolContext) -> dict:
    deals = [
        "Stay 3 nights, get 1 free (Standard & Deluxe rooms)",
        "20% off Executive Suites on weekends",
        "Family Room special: free kids’ meals with 2-night stay",
        "Penthouse Suite: Free spa access with booking before Aug 31"
    ]
    return {
        "status": "success",
        "current_deals": deals
    }


hotel_sales_agent = Agent(
    name="hotel_sales_agent",
    model="gemini-2.0-flash",
    description="Sales agent for promoting hotel rooms and packages",
    instruction="""
    You are the hotel sales agent. Your job is to help users explore available rooms, pricing, and current offers.

    <user_info>
    Name: {user_name}
    </user_info>

    <booking_info>
    User Bookings: {user_bookings}
    </booking_info>

    When users ask about rooms:
    1. Use the list_available_rooms tool to show options
    2. Offer recommendations based on their needs (luxury, family, budget)
    3. Use get_room_price to provide prices for specific room types
    4. If they seem price-conscious, suggest offers using offer_deals
    5. Encourage booking soon due to limited availability

    Sample Flow:
    - "Can you suggest a good room for a family?"
      → Use `list_available_rooms`, filter family-suited options
    - "How much is the Executive Suite?"
      → Use `get_room_price("Executive Suite")`
    - "Any deals right now?"
      → Use `offer_deals()`

    Be warm and persuasive, not pushy. Emphasize comfort, value, and convenience.
    """,
    tools=[list_available_rooms, get_room_price, offer_deals],
)
