# Code Quest 🏰

An interactive coding game that makes learning Python fun and engaging! Try it out at [Code Quest](https://code-quest-frontend-q50rd3li3-asaddus-projects.vercel.app/)

## Overview

Code Quest is a gamified coding platform where you can:
- Solve Python coding challenges of varying difficulty
- Earn XP and unlock achievements
- Get hints and view example solutions
- See real-time feedback on your code
- Learn through an engaging, fantasy-themed interface

## Features

### 🎮 Interactive Coding Environment
- Built-in Monaco code editor (same as VS Code)
- Real-time code execution
- Instant feedback on your solutions
- Support for Python with syntax highlighting

### 🏆 Progression System
- Earn XP for completing challenges
- Unlock achievements for special accomplishments
- Track your progress across multiple challenges
- Bonus XP for efficient solutions

### 📚 Learning Support
- Progressive hint system
- Example solutions with detailed explanations
- Clear error messages and feedback
- Test cases to validate your solutions

### 🎨 Modern UI
- Responsive design for all devices
- Dark theme for comfortable coding
- Clean and intuitive interface
- Real-time notifications for achievements

## Technical Stack

### Frontend
- React with TypeScript
- Vite for fast development and building
- Tailwind CSS for styling
- Monaco Editor for code editing
- WebSocket for real-time communication

### Backend
- FastAPI for the web framework
- WebSocket support for real-time features
- Safe code execution environment
- Automated test case validation

## Live Demo

Visit [Code Quest](https://code-quest-frontend-q50rd3li3-asaddus-projects.vercel.app/) to try it out!

Current Challenges:
1. **The Quest Begins**: Write your first battle cry function
2. **Dragon's Math**: Calculate sums using loops or mathematical formulas
3. **Magical Palindrome**: Check if words read the same forwards and backwards

## Development

### Prerequisites
- Node.js 16+
- Python 3.8+
- npm or yarn

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Asaddu/windsurf-claude-mcp-demo.git
cd windsurf-claude-mcp-demo
```

2. Install frontend dependencies:
```bash
cd frontend
npm install
```

3. Install backend dependencies:
```bash
cd backend
pip install -r requirements.txt
```

### Running Locally

1. Start the backend:
```bash
cd backend
uvicorn main:app --reload
```

2. Start the frontend:
```bash
cd frontend
npm run dev
```

Visit `http://localhost:5173` to see the app running locally.

## Deployment

The application is deployed on Vercel:
- Frontend: React application with Vite
- Backend: Python FastAPI with WebSocket support

## Security

- Safe code execution environment
- Protection against dangerous operations
- Isolated execution namespace
- Input validation and sanitization

## Future Plans

- More challenging coding problems
- Additional achievement types
- User accounts and persistence
- Leaderboards and social features
- More programming languages

## Contributing

Feel free to open issues or submit pull requests for:
- New coding challenges
- UI improvements
- Bug fixes
- Feature suggestions

## License

MIT License - feel free to use and modify!
