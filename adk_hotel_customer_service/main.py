# main.py

import asyncio

# Import the main hotel customer service agent
from hotel_customer_service_agent.agent import hotel_customer_service_agent
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from utils import add_user_query_to_history, call_agent_async, display_state

load_dotenv()

# ===== PART 1: Initialize In-Memory Session Service =====
session_service = InMemorySessionService()

# ===== PART 2: Define Initial State =====
initial_state = {
    "user_name": "Lakshay Rajput",
    "user_bookings": [],
    "interaction_history": [],
}

# use this for testing with bookings
# initial_state = {
#     "user_name": "Alex Rajput",
#     "user_bookings": [{
#         "room_id": "D-101",
#         "room_type": "Deluxe Room",
#         "check_in": "2024-11-15",
#         "check_out": "2024-11-18"
#     }],
#     "interaction_history": [],
# }


async def main_async():
    # Setup constants
    APP_NAME = "Hotel Support"
    USER_ID = "guest_alex"

    # ===== PART 3: Session Creation =====
    # --- ADD AWAIT HERE ---
    # create_session is an async function and must be awaited.
    new_session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        state=initial_state,
    )
    SESSION_ID = new_session.id
    print(f" Created new session: {SESSION_ID}")

    # ===== PART 4: Agent Runner Setup =====
    runner = Runner(
        agent=hotel_customer_service_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    # ===== PART 5: Interactive Conversation Loop =====
    print("\n Welcome to Hotel Customer Service Chat!")
    print("Type 'exit' or 'quit' to end the conversation.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("👋 Ending conversation. Goodbye!")
            break

        # Save the user message to state using our async utility function
        # --- ADD AWAIT HERE ---
        # add_user_query_to_history is now an async function and must be awaited.
        await add_user_query_to_history(
            session_service, APP_NAME, USER_ID, SESSION_ID, user_input
        )

        # Pass the input to the agent
        await call_agent_async(runner, USER_ID, SESSION_ID, user_input)

    # ===== PART 6: View Final Session State =====
    # We now use the async display_state function from utils.py, which is cleaner
    # and correctly handles the async call to get the session.
    print("\n🧠 Final Session State:")
    # --- ADD AWAIT HERE ---
    # display_state is now an async function and must be awaited.
    await display_state(session_service, APP_NAME, USER_ID, SESSION_ID, "Final State")


def main():
    # This is the standard way to run the top-level async function.
    asyncio.run(main_async())


if __name__ == "__main__":
    main()




