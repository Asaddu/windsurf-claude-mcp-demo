# Code Quest Demo

A fun web application for solving Python coding challenges with a modern React frontend and FastAPI backend.

## Features
- Interactive code editor with Python execution
- Real-time code validation
- Beautiful UI with Tailwind CSS
- WebSocket-based communication

## Tech Stack
- Backend: Python 3.10+, FastAPI
- Frontend: React 18, Tailwind CSS, Monaco Editor
- Development: Poetry, npm, Vite

## Getting Started

1. Install backend dependencies:
```bash
cd backend
poetry install
```

2. Install frontend dependencies:
```bash
cd frontend
npm install
```

3. Start the backend server:
```bash
cd backend
poetry run python main.py
```

4. Start the frontend development server:
```bash
cd frontend
npm run dev
```

5. Open http://localhost:5173 in your browser

## Development
- Backend runs on http://localhost:8000
- Frontend runs on http://localhost:5173
- WebSocket endpoint: ws://localhost:8000/ws
