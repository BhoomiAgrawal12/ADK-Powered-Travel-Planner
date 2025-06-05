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

activities_agent = Agent(
    name="activities_agent",
    model="gemini-2.0-flash",
    description="Suggests interesting activities for the user at a destination.",
    instruction=(
        "Given a destination, dates, and budget, suggest 2-3 engaging tourist or cultural activities. "
        "For each activity, provide a name, a short description, price estimate, and duration in hours. "
        "Respond in plain English. Keep it concise and well-formatted."
    )
)

session_service = InMemorySessionService()
runner = Runner(
    agent=activities_agent,
    app_name="activities_app",
    session_service=session_service
)
USER_ID = "user_activities"
SESSION_ID = "session_activities"

async def execute(request):
    logger.debug(f"Incoming request to activities agent: {request}")
    await session_service.create_session(
            app_name="activities_app",
            user_id=USER_ID,
            session_id=SESSION_ID
        )

    prompt = (
            f"Suggest activities in {request['destination']} "
            "Format each activity with these exact fields:\n"
            "- Activity name\n"
            "- Detailed description\n"
            "- Duration\n"
            "- Price range in INR\n"
            "- Location\n"
            "- Highlights (bullet list)\n"
            "Return as JSON with 'activities' array.Do not write any other text or markdown.\n"
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
                        "activities": parsed.get("activities", []),
                        "status": "success"
                    }
                except json.JSONDecodeError:
                    return {
                        "activities": [],
                        "status": "error",
                        "message": "Failed to parse activities data"
                    }