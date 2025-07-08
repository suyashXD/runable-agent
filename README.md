# Coding Agent with Sandboxing

A Docker-based coding agent system with GUI capabilities, context management, and orchestration layer for automated task execution.

## Architecture

- **Agent Container**: Ubuntu-based environment with VNC, noVNC, Jupyter, and development tools
- **Context Management**: Token-limited context persistence with intelligent pruning
- **Orchestration**: FastAPI server managing containerized job execution

## Quick Start

### 1. Build Agent Image
```bash
cd agent
docker build -t agent-image .
```

### 2. Start Orchestrator
```bash
cd orchestrator
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 3. Submit Task
```bash
curl -X POST "http://localhost:8000/submit" \
  -H "Content-Type: application/json" \
  -d '{"task": "Build me a todo app in React"}'
```

### 4. Check Status
```bash
curl "http://localhost:8000/status/{job_id}"
```

## API Endpoints

- `POST /submit` - Submit a coding task, returns job ID
- `GET /status/{job_id}` - Check job status and get download link when complete

## Features

- **Sandboxed Execution**: Each job runs in isolated Docker container
- **GUI Access**: VNC server (port 5900) and noVNC web interface (port 6080)
- **Context Management**: Automatic pruning when exceeding 1M token limit
- **File Downloads**: Completed projects available as ZIP archives

## Directory Structure

```
├── agent/                  # Agent container files
│   ├── Dockerfile         # Agent environment setup
│   ├── agent_start.sh     # Task execution script
│   ├── context_manager.py # Context persistence & pruning
│   └── supervisord.conf   # Service management
├── orchestrator/          # Orchestration server
│   ├── main.py           # FastAPI server
│   └── requirements.txt  # Python dependencies
├── workspaces/           # Job workspaces (auto-created)
└── downloads/            # Completed job archives
```

## Security

- Container isolation for each job
- No persistent data between jobs
- Automatic cleanup after completion

## Context Management

The system handles large contexts by:
- Tracking token usage (4 bytes per token)
- Pruning older content when approaching 1M token limit
- Maintaining execution state in `/workspace/context.txt`

## Requirements

- Docker
- Python 3.8+
- FastAPI dependencies (see requirements.txt)
