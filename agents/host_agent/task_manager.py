from common.a2a_client import call_agent
import json
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
def sanitize_url(url):
    return url.strip().replace("\t", "").replace("\n", "").replace(" ", "")

FLIGHT_URL = sanitize_url("http://localhost:8001/run")
STAY_URL = sanitize_url("http://localhost:8002/run")
ACTIVITIES_URL = sanitize_url("http://localhost:8003/run")

def format_flights_markdown(flights):
    if not flights or len(flights) == 0:
        return "No flight options available."
    
    markdown = "### Available Flights:\n\n"
    for flight in flights:
        markdown += f"* **{flight.get('Airline name', 'Airline')}**\n"
        markdown += f"  * Flight: {flight.get('Flight number', 'N/A')}\n"
        markdown += f"  * Departure: {flight.get('Departure time and date', 'N/A')}\n"
        markdown += f"  * Return: {flight.get('Return time and date', 'N/A')}\n"
        markdown += f"  * Price: ₹{flight.get('Price in INR', 'N/A')}\n"
        markdown += f"  * Type: {flight.get('Route type', 'N/A')}\n\n"
    return markdown
def format_stays_markdown(stays):
    if not stays or len(stays) == 0:
        return "No stay options available."
    
    markdown = "### Accommodation Options:\n\n"
    for stay in stays:
        markdown += f"* **{stay.get('Property name', 'Accommodation')}**\n"
        markdown += f"  * Type: {stay.get('Type', 'N/A')}\n"
        markdown += f"  * Location: {stay.get('Location', 'N/A')}\n"
        markdown += f"  * Price: {stay.get('Price per night in INRe', 'N/A')}\n"
        markdown += f"  * Rating: {stay.get('Rating', 'N/A')}\n\n"
        Amenities = stay.get('Amenities', [])
        if Amenities:
            markdown += "  *Amenities:\n"
            for Ameniti in Amenities:
                markdown += f"    * {Ameniti}\n"
        markdown += "\n"
    return markdown

def format_activities_markdown(activities):
    if not activities or len(activities) == 0:
        return "No activities available."
    
    markdown = "### Suggested Activities:\n\n"
    for activity in activities:
        markdown += f"* **{activity.get('Activity name', 'Activity')}**\n"
        markdown += f"  * {activity.get('Detailed description', 'No description available')}\n"
        markdown += f"  * Duration: {activity.get('Duration', 'N/A')}\n"
        markdown += f"  * Price: {activity.get('Price range in INR', 'N/A')}\n"
        markdown += f"  * Location: {activity.get('Location', 'N/A')}\n\n"
        highlights = activity.get('Highlights', [])
        if highlights:
            markdown += "  * Highlights:\n"
            for highlight in highlights:
                markdown += f"    * {highlight}\n"
        markdown += "\n"
    return markdown
async def run(payload):
    try:
        flights = await call_agent(FLIGHT_URL, payload)
        logger.debug(f"Raw flights response: {flights}")

        stays = await call_agent(STAY_URL, payload)
        logger.debug(f"Raw stays response: {stays}")

        activities = await call_agent(ACTIVITIES_URL, payload)
    
        # Parse responses
        flights_data = json.loads(flights) if isinstance(flights, str) else flights
        logger.debug(f"Parsed flights data: {flights_data}")

        stays_data = json.loads(stays) if isinstance(stays, str) else stays
        logger.debug(f"Parsed stays data: {stays_data}")

        activities_data = json.loads(activities) if isinstance(activities, str) else activities
        
        print("Flights data:", flights_data)
        print("Stays data:", stays_data)
        print("Activities data:", activities_data)
        return {
            "flights": format_flights_markdown(flights_data.get("flights", [])),
            "stay": format_stays_markdown(stays_data.get("stay", [])),
            "activities": format_activities_markdown(activities_data.get("activities", []))
        }
    except Exception as e:
        return {
            "flights": "Error fetching flight data.",
            "stay": "Error fetching stay data.",
            "activities": "Error fetching activities data."
        }