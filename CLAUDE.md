# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**tminn** is a multi-agent AI management system that coordinates different AI agents (Project Manager, Software Engineers, Business Analyst, Tester) working collaboratively on projects. Built as a Flask web application using the OpenAI Agents SDK for agent orchestration.

## Development Commands

### Python Backend
```bash
# Run the main Flask application
python run.py

# Run the background scheduler for agent coordination
python scheduler.py

# Run tests
python -m pytest

# Lint code
python -m flake8

# Install dependencies
pip install -r requirements.txt
```

### Frontend Build
```bash
# Production build
npm run build

# Development build with watch mode
npm run dev

# Install frontend dependencies
npm install
```

## Architecture Overview

### Multi-Agent System
The core architecture implements a collaborative AI agent framework:

- **PM Agent** (`app/agency/pm/`): Project management and task coordination
- **Business Analyst** (`app/agency/business_analyst/`): Requirements gathering
- **Software Engineers** (`app/agency/se1/`, `app/agency/se2/`): Code development
- **Tester** (`app/agency/tester/`): Quality assurance

### Technology Stack

**Backend:**
- Flask 3.1.1 with dependency injection (Flask-Injector)
- OpenAI Agents SDK 0.0.17 for agent orchestration
- MongoDB 4.10.1 with repository pattern
- APScheduler 3.11.0 for background task coordination

**Frontend:**
- Alpine.js 3.14.9 for reactive UI
- Bootstrap 5.3.6 with Bootswatch themes
- Webpack 5.99.9 build system
- TypeScript and SCSS support

### Data Layer
- **MongoDB Collections**: `messages` and `tasks`
- **Repository Pattern**: `tasks_repository.py` and `messages_repository.py`
- **Connection**: Singleton MongoClient with dependency injection
- **DNS Configuration**: Custom resolver for Android/Termux compatibility

### Agent Communication
- Shared MongoDB for task and message coordination
- APScheduler with MongoDB job store for persistent scheduling
- Tools and handoffs for inter-agent communication patterns

## Key Implementation Details

### Dependency Injection
The project uses Flask-Injector for loose coupling. All services are configured in `app/services/service.py` and injected throughout the application.

### MongoDB Integration
Custom DNS resolver configuration in `app/db/mongodb.py` addresses Android/Termux restrictions on `/etc/resolv.conf` access.

### Agent Tools
Each agent directory contains:
- Agent definition and configuration
- Specialized tools for that agent's role
- Handoff mechanisms for collaboration

### Background Processing
`scheduler.py` runs agent coordination tasks using APScheduler with MongoDB persistence, allowing agents to wake up periodically and process tasks.

## Code Quality

- **Linting**: flake8 with 160 character line length limit
- **Testing**: pytest framework with tests in `tests/` directory
- **Type Safety**: TypeScript for frontend code
- **Exclusions**: Standard exclusions for git, cache, and virtual environment directories

## Development Notes

- Project is optimized for Android/Termux development environment
- Frontend LLM module has pending typo fix (`thinkink` → `thinking`)
- Agent behavior patterns are designed to be emergent and experimental
- Architecture follows "keep it simple as a stick" philosophy

## Testing

Run the test suite with `python -m pytest`. Tests cover:
- Agent functionality (`test_agent.py`)
- Flask application structure (`test_app.py`)

## Build Artifacts

Frontend builds generate static assets that are served by Flask:
- Webpack bundles JavaScript and SCSS
- Static files served from Flask templates
- Bootstrap and Alpine.js integration