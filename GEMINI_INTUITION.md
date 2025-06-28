# Project Intuition

This project appears to be a web application, likely built with Python (Flask, given the `app/routes`, `app/templates`, and `app/static` directories) for the backend and a JavaScript/TypeScript frontend.

## Backend (Python)
- **Framework:** Likely Flask, indicated by the directory structure (`app/routes`, `app/templates`, `app/static`).
- **Agents/AI:** The `app/agency` directory with subdirectories like `business_analyst`, `pm`, `se1`, `se2`, and `tester` strongly suggests an AI agent-based system. The `pm_agent.py` and `tools.py` within `app/agency/pm` further support this. This could be a system where AI agents collaborate to manage or develop projects.
- **Database:** `app/db` with `messages_repository.py`, `mongodb.py`, and `tasks_repository.py` indicates MongoDB is used for data persistence, likely storing messages and tasks related to the agents.
- **Services:** `app/services/service.py` suggests a service layer for business logic.
- **Configuration:** `app/config.py` for application configuration.
- **Entry Point:** `run.py` is likely the main script to start the application.
- **Scheduler:** `scheduler.py` suggests some form of task scheduling or background processing.

## Frontend (JavaScript/TypeScript, SCSS)
- **Technologies:** `frontend/js` with `core.ts`, `index.js`, and `llm.js` points to a JavaScript/TypeScript frontend. `frontend/scss` with `claude-variables.scss` and `main.scss` indicates SCSS for styling.
- **Bundling:** `webpack.config.js` suggests Webpack is used for bundling frontend assets.
- **Dependencies:** `package.json` and `package-lock.json` confirm Node.js/npm for frontend dependency management.
- **Images:** `frontend/images` for static assets.

## Overall
- **Purpose:** The combination of AI agents, task management, and a web interface suggests an application designed to automate or assist in project management, software development, or a similar domain, possibly using large language models (LLMs) given `frontend/js/src/llm.js` and `documentation/openai_agents_documentation.md`.
- **Testing:** The `tests` directory with `test_agent.py` and `test_app.py` indicates unit/integration tests are in place for both the agent logic and the application.
- **Documentation:** `README.md`, `DEV_INTUITION.md`, `IDEAS.md`, `KANBAN.md`, and `documentation/openai_agents_documentation.md` suggest a well-documented project with a focus on development processes and AI agent specifics.

This project seems to be a sophisticated system leveraging AI agents for some form of automated workflow, exposed through a web interface, with a clear separation of concerns between frontend and backend.
