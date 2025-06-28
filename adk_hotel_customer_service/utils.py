from datetime import datetime
from google.genai import types

# ANSI color codes for terminal output
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"

async def update_interaction_history(session_service, app_name, user_id, session_id, entry):
    try:
        session = await session_service.get_session(
            app_name=app_name, user_id=user_id, session_id=session_id
        )
        interaction_history = session.state.get("interaction_history", [])
        if "timestamp" not in entry:
            entry["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        interaction_history.append(entry)
        updated_state = session.state.copy()
        updated_state["interaction_history"] = interaction_history
        await session_service.create_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id,
            state=updated_state,
        )
    except Exception as e:
        print(f"Error updating interaction history: {e}")

async def add_user_query_to_history(session_service, app_name, user_id, session_id, query):
    await update_interaction_history(
        session_service,
        app_name,
        user_id,
        session_id,
        {
            "action": "user_query",
            "query": query,
        },
    )

async def add_agent_response_to_history(session_service, app_name, user_id, session_id, agent_name, response):
    await update_interaction_history(
        session_service,
        app_name,
        user_id,
        session_id,
        {
            "action": "agent_response",
            "agent": agent_name,
            "response": response,
        },
    )

async def display_state(session_service, app_name, user_id, session_id, label="Current State"):
    try:
        session = await session_service.get_session(app_name=app_name, user_id=user_id, session_id=session_id)
        print(f"\n{'-' * 10} {label} {'-' * 10}")
        print(f"👤 User: {session.state.get('user_name', 'Unknown')}")

        user_bookings = session.state.get("user_bookings", [])
        if user_bookings and any(user_bookings):
            print("🏨 Bookings:")
            for b in user_bookings:
                if isinstance(b, dict):
                    room = b.get("room_type", "Unknown Room")
                    check_in = b.get("check_in", "N/A")
                    check_out = b.get("check_out", "N/A")
                    print(f"  - {room}: {check_in} to {check_out}")
                elif b:
                    print(f"  - {b}")
        else:
            print("🏨 Bookings: None")

        interaction_history = session.state.get("interaction_history", [])
        if interaction_history:
            print("📝 Interaction History:")
            for idx, i in enumerate(interaction_history, 1):
                if isinstance(i, dict):
                    action = i.get("action", "interaction")
                    timestamp = i.get("timestamp", "unknown time")
                    if action == "user_query":
                        print(f'  {idx}. User query at {timestamp}: "{i.get("query", "")}"')
                    elif action == "agent_response":
                        resp = i.get("response", "")
                        if len(resp) > 100:
                            resp = resp[:97] + "..."
                        print(f'  {idx}. {i.get("agent", "unknown")} response at {timestamp}: "{resp}"')
                    else:
                        detail = ", ".join(f"{k}: {v}" for k, v in i.items() if k not in ["action", "timestamp"])
                        print(f"  {idx}. {action} at {timestamp}" + (f" ({detail})" if detail else ""))
                else:
                    print(f"  {idx}. {i}")
        else:
            print("📝 Interaction History: None")

        extra_keys = [k for k in session.state if k not in ["user_name", "user_bookings", "interaction_history"]]
        if extra_keys:
            print("🔑 Additional State:")
            for k in extra_keys:
                print(f"  {k}: {session.state[k]}")
        print("-" * (22 + len(label)))
    except Exception as e:
        print(f"Error displaying state: {e}")

async def process_agent_response(event):
    print(f"Event ID: {event.id}, Author: {event.author}")
    has_specific_part = False
    if event.content and event.content.parts:
        for part in event.content.parts:
            if hasattr(part, "text") and part.text and not part.text.isspace():
                print(f"  Text: '{part.text.strip()}'")

    final_response = None
    if not has_specific_part and event.is_final_response():
        if (
            event.content
            and event.content.parts
            and hasattr(event.content.parts[0], "text")
            and event.content.parts[0].text
        ):
            final_response = event.content.parts[0].text.strip()
            print(f"\n{Colors.BG_BLUE}{Colors.WHITE}{Colors.BOLD}╔══ AGENT RESPONSE ═════════════════════════════════════════{Colors.RESET}")
            print(f"{Colors.CYAN}{Colors.BOLD}{final_response}{Colors.RESET}")
            print(f"{Colors.BG_BLUE}{Colors.WHITE}{Colors.BOLD}╚═════════════════════════════════════════════════════════════{Colors.RESET}\n")
        else:
            print(f"\n{Colors.BG_RED}{Colors.WHITE}{Colors.BOLD}==> Final Agent Response: [No text content in final event]{Colors.RESET}\n")
    return final_response

async def call_agent_async(runner, user_id, session_id, query):
    content = types.Content(role="user", parts=[types.Part(text=query)])
    print(f"\n{Colors.BG_GREEN}{Colors.BLACK}{Colors.BOLD}--- Running Query: {query} ---{Colors.RESET}")
    final_response_text = None
    agent_name = None

    await display_state(runner.session_service, runner.app_name, user_id, session_id, "State BEFORE processing")

    try:
        async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
            if event.author:
                agent_name = event.author
            response = await process_agent_response(event)
            if response:
                final_response_text = response
    except Exception as e:
        print(f"{Colors.BG_RED}{Colors.WHITE}ERROR during agent run: {e}{Colors.RESET}")

    if final_response_text and agent_name:
        await add_agent_response_to_history(
            runner.session_service,
            runner.app_name,
            user_id,
            session_id,
            agent_name,
            final_response_text,
        )

    await display_state(runner.session_service, runner.app_name, user_id, session_id, "State AFTER processing")
    print(f"{Colors.YELLOW}{'-' * 30}{Colors.RESET}")
    return final_response_text
