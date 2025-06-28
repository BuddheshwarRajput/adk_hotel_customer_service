# Hierarchical AI Hotel Concierge 🏨✨

This project is an advanced, conversational AI bot built with the Google Agent Development Kit (ADK). It simulates a hotel's customer service department by using a hierarchical structure of specialized AI agents to handle a wide range of guest queries.

The system features a main "router" agent that understands user intent and delegates tasks to a team of specialists, including a Sales Agent, a Policy Agent, a Booking Agent, and a Room Support Agent.


*   **Hierarchical Agent Architecture:** A main agent manages and routes tasks to four specialized sub-agents.
*   **Stateful Conversations:** The bot maintains session state, remembering user details and booking information across multiple turns.
*   **Advanced Tool Use:** Each specialist agent is equipped with a set of tools (functions) to perform specific actions like checking prices, getting policies, or modifying bookings.
*   **Complex Query Handling:** The system is designed to break down multi-part user queries and orchestrate responses from multiple sub-agents.
*   **Natural Language Interaction:** Users interact with the bot through a simple command-line interface.



The project follows a "Manager and Specialists" pattern:

1.  **`hotel_customer_service_agent` (The Manager/Router):**
    *   This is the top-level agent.
    *   Its sole responsibility is to analyze the user's query and route it to the most appropriate sub-agent. It does not answer questions directly.

2.  **`sub_agents` (The Specialists):**
    *   **`hotel_sales_agent`:** Handles all pre-booking inquiries. Equipped with tools to list rooms, check prices, and offer deals.
    *   **`policy_agent`:** The hotel's rulebook. Equipped with tools to answer questions about check-in/out times, pets, refunds, and ID requirements.
    *   **`booking_agent`:** Manages existing reservations. Equipped with tools to view booking history, and process cancellations and refunds.
    *   **`room_support_agent`:** Assists guests who have an active booking. Equipped with tools to check room features, find upgrade options, and report issues.


*   Python 3.8+
*   Google Agent Development Kit (`adk`)
*   Python Dotenv (`python-dotenv`) for environment variable management

