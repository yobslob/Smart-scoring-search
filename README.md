# Search Engine

This project is an investor-side Smart Search Engine. It helps investors to find the most favourable and profitable startups according their affinity alignment.<br>
As the engine ranks the most suitable startups within a platform that connects investors, startups, brokers, and freelancers.
## About

This project was part of my internship at Prodigal AI. It's a key piece of a new startup platform designed to bring together investors, startups, brokers, and freelancers. My part, the Smart Search Engine for investors, is a helpful tool that:

- Shows investors a ranked sorted list of startups that are a great fit for them.
- Uses a special "affinity score" to match what investors are looking for with what startups offer.
- Employs semantic search and vector embedding to understand the meaning behind search terms and startup descriptions, not just keywords.
- Includes a "profitability score" to highlight startups that look financially promising.
- Gives each startup an overall relevance score out of 100, making it easier for investors to make smart decisions.
<br>
Currently, only local-host is supported. Working on deploying it on custom server without losing accuracy.

> You’ll need Chrome browser to get the best experience.

<br>

Here’s a preview of the webApp:  
![Dashboard](frontend/public/searchPage.png)
<br>

## Tech Stack

### Frontend
- Next.js
- TailwindCSS

### Backend 
- FastAPI
- Uvicorn
- Redis
- Python
- PyMongo

### Database
- MongoDB

### Model
- LangChain
- LangChain-Google-GenAi
- LangChain-Community

  
# Project Setup

### Pre-requisites

- Obtain a Google API key from Google AI Studio.
- Create a .env file in the backend folder (details provided below).

### Setting up Redis
These instructions are for setting up Redis on Windows using WSL (Windows Subsystem for Linux). Ensure WSL is installed.

1. Open a command prompt as an administrator.
2. Install WSL if not already installed:

```bash
wsl --install
```

3. Launch WSL:
```bash
wsl
```

4. Add the Redis repository:
```bash
curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list

```

5. Update package lists and install Redis:
```bash
sudo apt-get update
sudo apt-get install redis
```

6. Start the Redis server:
```bash
sudo service redis-server start
```

7. Edit the Redis configuration file:
  - Open the file with:
  ```bash
  sudo nano /etc/redis/redis.conf
  ```
  - A vim environment will show a config file. <br>Make these changes:
  ```bash
  Change bind 127.0.0.1 ::1 -> bind 0.0.0.0
  Change protected-mode yes -> protected-mode no
  Comment out 'requirepass foobared' by removing '#' from the beginning
  # requirepass foobared -> requirepass your_password
  Save with Ctrl + O, press Enter, and exit with Ctrl + X
  ```

8. Restart the Redis server:
```bash
sudo service redis-server restart
```

9. Verify Redis is running:
```bash
redis-cli -a your_password
```


### Backend Setup

1. Open a command prompt in the project’s root directory.
2. Navigate to the backend directory:
```bash
cd backend
```

3. Create a virtual environment:
```bash
python -m venv venv
```

4. Activate the virtual environment:
```bash
On Windows: venv\Scripts\activate

On macOS/Linux: source venv/bin/activate
```



5. Install required packages:
```bash
pip install -r requirements.txt
```

6. Run the backend server:
```bash
uvicorn main:app --reload
```


### Frontend Setup

1. Open another command prompt in the project’s root directory.
2. Navigate to the frontend directory:cd frontend


3. Install dependencies:
```bash
npm install
```

4. Run the development server:
```bash
npm run dev
```


### .env File Structure
Place this in the backend folder:
```bash
MONGO_URI=mongodb+srv:***********
GOOGLE_API_KEY=AIzaSyD***********
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_PASSWORD=your_password
```

- Replace your_password with your Redis password.
- Ensure the GOOGLE_API_KEY matches your actual key.

## POST /search

<b>Purpose</b>: Accepts an investor search request (plain text + filters), constructs an investor profile (using an environment-configured investor id as baseline), parses the text query (via cache/LLM helper), fetches candidate startups from the database, runs scoring, and returns a ranked list of startups.

<b>URL</b>: /search

<b>Method</b>: POST

<b>CORS</b>: Allowed origin configured for http://localhost:3000 in the app middleware.

<b>Request Body (JSON)</b>
```bash
{
  "keyword": "AI for logistics",
  "stage_preferences": ["Seed", "Series A"],
  "sector_focus": ["Logistics", "SaaS"],
  "regions_preferred": ["India", "South Asia"]
}
```
Field descriptions:

- keyword (string): free-text search query provided by the investor. This is parsed by get_parsed_query() prior to database retrieval. Required.
- stage_preferences (array of strings): optional list of preferred funding stages (e.g., Pre-seed, Seed, Series A). May be empty.
- sector_focus (array of strings): optional list of preferred sectors/industries. If empty, the parsed primary industry may be used.
- regions_preferred (array of strings): optional list of preferred location regions/countries.

Behavior summary (server side):

- The server obtains a baseline investor profile using get_investor_profile(INVESTOR_ID) where INVESTOR_ID is read from the environment. If the call returns None, an empty profile string is used as the base.
- Any runtime filters provided in the request are appended to the investor profile text before scoring.
- get_parsed_query(keyword) is called to convert the keyword into structured values: text_search, primary_industry, stage_preferences, and regions_preferred. The function may use a cache or a lightweight LLM/heuristic.

Final filters are derived as follows:

- industry_filter is taken from sector_focus if provided; otherwise from parsed['primary_industry'] when not 'None'.
- stage_prefs are taken from stage_preferences request field or the parsed query fallback.
- regions are taken from regions_preferred request field or the parsed query fallback.

search_startups(...) is called with industry_filter, text_query (parsed), stage_preferences, and regions_preferred to fetch candidate startup profiles from the DB.

If no startups are returned, the endpoint responds with an empty JSON array [] and HTTP 200.

If startups are returned, score_startups(investor_profile, startups) is called to compute final scores and ranking. The sorted list is returned as the response.

Example response (success):
```bash
[
  {
    "startup_id": "s_001",
    "name": "LogiAI",
    "final_score": 86.4,
    "semantic_score": 90.1,
    "profitability_score": 78.2,
    "tags": ["Perfect Fit", "Strong Unit Economics"],
    "metrics": {"MRR": 12000, "CAC": 30, "monthly_users": 4000}
  },
  {
    "startup_id": "s_002",
    "name": "FleetSense",
    "final_score": 79.5,
    "semantic_score": 85.3,
    "profitability_score": 66.7,
    "tags": ["Good Intent Match", "Early Traction"],
    "metrics": {"MRR": 3500, "CAC": 55, "monthly_users": 900}
  }
]
```
Status codes:

- 200 OK: Successful response. May return an empty array if no matching startups are found.
- 4xx client errors: FastAPI will return 422 Unprocessable Entity for invalid request JSON / schema violations.
- 5xx server errors: unhandled exceptions will surface as 500 unless explicitly caught. Consider wrapping critical calls with try/except and returning 503 Service Unavailable or a helpful error object for predictable failure modes.

Logging & debug traces: main.py logs debug prints to stdout for key steps: received request payload, parsed query content, final derived filters, number of startups fetched, and investor profile text used for scoring. This helps during local development but should be replaced by structured logging for production (e.g., loguru or Python logging with JSON output).

Environment variables:

INVESTOR_ID — a baseline investor identifier used to fetch stored investor profile with get_investor_profile().

### Notes

> For testing, use the Chrome browser for better frontend integration.
