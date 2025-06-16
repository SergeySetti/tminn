 # Developer Intuition and Brain Dump

 Here’s my initial gathered intuition about the tminn project:

 - Project name: “tminn”
 - Purpose: Experimental AI “team” framework with multiple agent roles communicating via shared MongoDB channel and driven by scheduled tasks.
 - Tech stack:
   - Backend: Python 3, Flask + Flask-Injector, APScheduler with MongoDBJobStore, PyMongo
   - Frontend: Alpine.js + Boxicons + Bootstrap/Bootswatch, bundled via Webpack (JS + SCSS)
   - DB/State: MongoDB for both data collections and job store / agent communication channel
     - `tminn` database with collections:
       - `messages` – shared channel for agent communication
       - `jobs` – APScheduler job store
       - `tasks` – task definitions for agents
       - `agents` – agent metadata (name, role, status, etc.)
 - Key components:
   - app/:
     - config.py – loads secrets from .env (SECRET_KEY, DB URI, OPENAI API keys, etc.)
     - routes/main.py – serves index.html and /health endpoint
     - services/service.py – DI module: provides MongoClient and wraps Db class
     - db/mongodb.py – PyMongo wrapper for collections and helper methods
     - agency/… – scaffolding for AI-agent logic; Business Analyst has initial JSON background
   - scheduler.py – wires APScheduler (with DI) and schedules tasks; currently only a “tick” job
   - run.py – Flask entrypoint
   - frontend/ – source (JS/TS, SCSS, images); built assets land in app/static/core/
   - tests/ – minimal unittest verifying home page
   - KANBAN.md – backlog: scheduler done, next up “Add first task type for PM AI Agent”
   - IDEAS.md – high-level shared message channel ideas
 - Observations & next steps:
   - DI and scheduler plumbing is in place; tick job exists
   - Need to define and schedule PM agent’s first task cycle to read/write to MongoDB
   - Frontend AlpineJS stub has a typo in toggle (thinkink vs thinking); demo-only
   - requirements.txt is garbled (null bytes) and may need regeneration
   - No env sample or docs for required env vars; consider adding .env.example
   - Tests are sparse; add tests around scheduler job registration and agent logic

 Next move: implement the PM AI agent’s scheduled job and the shared message channel logic.
