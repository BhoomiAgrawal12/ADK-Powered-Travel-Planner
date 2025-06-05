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
stay_agent = Agent(
    name="stay_agent",
    model="gemini-2.0-flash",
    description="Suggests stay options for a destination.",
    instruction=(
        "Given a destination, travel dates, and budget, suggest few stay options. "
        "Include stay type,location, food available, and price. Ensure stay fit within the budget."
    )
)

session_service = InMemorySessionService()
runner = Runner(
    agent=stay_agent,
    app_name="stay_app",
    session_service=session_service
)

USER_ID = "user_2"
SESSION_ID = "session_002"

async def execute(request):
    logger.debug(f"Incoming request to stay agent: {request}")
    await session_service.create_session(
            app_name="stay_app",
            user_id=USER_ID,
            session_id=SESSION_ID
        )

        # Format prompt to match expected JSON structure
        
    prompt = (
            f"Find accommodations in {request['destination']} "
            f"from {request['start_date']} to {request['end_date']} "
            f"within budget {request['budget']}. "
            "Format each stay option with these exact fields:\n"
            "- Property name\n"
            "- Type (hotel/resort/hostel)\n"
            "- Location details\n"
            "- Price per night in INR\n"
            "- Rating (out of 5)\n"
            "- Amenities (bullet list)\n"
            "Return as JSON with 'stay' array.Do not write any other text or markdown.\n"
        )

    message = types.Content(role="user", parts=[types.Part(text=prompt)])

    try:      
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
                    return parsed
                except json.JSONDecodeError as e:
                    logger.error(f"JSON parsing error: {e}")
                    return {"stay": []}         
    except Exception as e:
        logger.error(f"Error in stay agent execution: {e}")
        return {
            "stay": [],
            "status": "error",
            "message": str(e)
        }