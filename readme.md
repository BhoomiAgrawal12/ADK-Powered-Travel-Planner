# ADK-Powered Multi-Agent Travel Planner

A modular AI-powered travel planning system that uses Google’s Agent Development Kit (ADK) to coordinate various travel tasks like flight search, stay and activity suggestions through dedicated agents.

---

## Features

- Multi-Agent System using Google's ADK
- Flight Agent: Suggests flight options.
- Stay Agent: Recommends accommodations.
- Activities Agent: Recommends top local attractions.
- Host Agent: Orchestrates all agents and compiles results.
- Streamlit Frontend: User-friendly UI for travel planning.

---

## Architecture



```

User → Streamlit UI → Host Agent → \[Flight Agent, Stay Agent, Activities Agent]
↑             ↑              ↑
Uvicorn       Uvicorn        Uvicorn

```

Each agent runs independently on a different port using FastAPI & Uvicorn.

---

## Project Structure

```

project-root/
│
├── agents/
│   ├── host\_agent/
│   │   └── **main**.py
│   ├── flight\_agent/
│   │   └── **main**.py
│   ├── stay\_agent/
│   │   └── **main**.py
│   └── activities\_agent/
│       └── **main**.py
│
├── common/
│   └── a2a\_client.py         # Utility to call other agents
│
├── travel\_ui.py              # Streamlit frontend
└── README.md

````

---

## Requirements

- Python 3.10+
- google-adk
- streamlit
- httpx
- uvicorn
- fastapi

Install dependencies:

```bash
pip install -r requirements.txt
````

---

## Running the Project (Windows Instructions)

In PowerShell, open 4 new terminal windows/tabs and run:

```powershell
start cmd /k "uvicorn agents.host_agent.__main__:app --port 8000"
start cmd /k "uvicorn agents.flight_agent.__main__:app --port 8001"
start cmd /k "uvicorn agents.stay_agent.__main__:app --port 8002"
start cmd /k "uvicorn agents.activities_agent.__main__:app --port 8003"
```

Then in a fifth terminal, run the frontend:

```powershell
streamlit run travel_ui.py
```

---

## Usage

* Enter travel details in the Streamlit UI.
* Click "Plan My Trip".
* The host agent will collect responses from the other agents.
* You'll see:

  * Flight options
  * Stay suggestions
  * Top activities

---

## Troubleshooting

* 500 Errors: Ensure all agents are running and return valid JSON dictionaries.
* Invalid URL: Watch out for hidden characters (`\t`, spaces, etc.) in URLs.
* Model Overload: If Gemini is overloaded, retry after a short delay.

---

## Notes

* Built with [Google's Agent Development Kit (ADK)](https://ai.google.dev/docs/agents)
* Uses Gemini 2.0 Flash model
* Easily extendable by adding more specialized agents.

---

## Future Improvements

* Better error handling & retries
* Caching agent responses
* Add maps or visuals in the frontend
* Authentication support for personalized planning
