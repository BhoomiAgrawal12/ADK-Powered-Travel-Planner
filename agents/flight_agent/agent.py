from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import json
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
flight_agent = Agent(
    name="flight_agent",
    model="gemini-2.0-flash",
    description="Suggests flight options for a destination.",
    instruction=(
        "Given a destination, travel dates, and budget, suggest 1-2 realistic flight options. "
        "Include airline name, price, and departure time. Ensure flights fit within the budget."
    )
)

session_service = InMemorySessionService()
runner = Runner(
    agent=flight_agent,
    app_name="flight_app",
    session_service=session_service
)

USER_ID = "user_1"
SESSION_ID = "session_001"


async def execute(request):
    print("Executing flight agent with request:", request)
    await session_service.create_session(
        app_name="flight_app",
        user_id=USER_ID,
        session_id=SESSION_ID
    )

    prompt = (
            f"Find flights from {request['origin']} to {request['destination']} "
            f"from {request['start_date']} to {request['end_date']} "
            f"within budget {request['budget']}. "
            "Format each flight option with these exact fields:\n"
            "- Airline name\n"
            "- Flight number\n"
            "- Departure time and date\n"
            "- Return time and date\n"
            "- Price in INR\n"
            "- Route type (direct/layover)\n"
            "Return as JSON with 'flights' array."
        )
    
    message = types.Content(role="user", parts=[types.Part(text=prompt)])
    async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=message):
            if event.is_final_response():
                response_text = event.content.parts[0].text
                response_text = response_text.strip()
                if response_text.startswith("```json"):
                    response_text = response_text[7:]
                if response_text.startswith("```"):
                    response_text = response_text[3:]
                if response_text.endswith("```"):
                    response_text = response_text[:-3]
                response_text = response_text.strip()
                try:
                    parsed = json.loads(response_text)
                    return {
                        "flights": parsed.get("flights", []),
                        "status": "success"
                    }
                except json.JSONDecodeError:
                    return {
                        "flights": [],
                        "status": "error",
                        "message": "Failed to parse flight data"
                    }