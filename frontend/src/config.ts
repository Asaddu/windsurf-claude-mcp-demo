const isProd = import.meta.env.PROD

export const API_URL = isProd
  ? 'https://windsurf-claude-mcp-demo-backend.vercel.app'
  : 'http://localhost:8000'

export const WS_URL = isProd
  ? 'wss://windsurf-claude-mcp-demo-backend.vercel.app/ws'
  : 'ws://localhost:8000/ws'
