# CHANGE THIS FILE

# 1. Import the parent agent (which now has no dependencies)
from .agent import hotel_customer_service_agent

# 2. Import all the sub-agents
from .sub_agents.policy_agent.agent import policy_agent
from .sub_agents.hotel_sales_agent.agent import hotel_sales_agent
from .sub_agents.room_support_agent.agent import room_support_agent
from .sub_agents.booking_agent.agent import booking_agent

# 3. Assemble the hierarchy. This is the magic step!
# We are modifying the parent agent object *after* all agents have been imported.
hotel_customer_service_agent.sub_agents = [
    policy_agent,
    hotel_sales_agent,
    room_support_agent,
    booking_agent,
]