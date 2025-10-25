# Billionaire Arbitrage System - Frontend

This is the frontend dashboard for the Billionaire Arbitrage System, built with Next.js, React, and Material-UI.

## Features

- Real-time system health monitoring
- DeFi pool visualization
- Live arbitrage opportunity tracking
- WebSocket integration for real-time updates
- Material-UI dark theme

## Getting Started

### Prerequisites

- Node.js 18+ installed
- Backend API running on http://localhost:8000

### Installation

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

The dashboard will be available at [http://localhost:3000](http://localhost:3000)

## Configuration

### API URL

By default, the frontend connects to the backend at `http://localhost:8000`. To change this, set the `NEXT_PUBLIC_API_URL` environment variable:

```bash
# .env.local
NEXT_PUBLIC_API_URL=http://your-backend-url:8000
```

## Development

The frontend structure:

```
frontend/
├── src/
│   ├── pages/          # Next.js pages
│   ├── components/     # React components
│   └── styles/         # Global styles
├── public/             # Static assets
└── package.json        # Dependencies
```

## Available Scripts

- `npm run dev` - Start development server with hot reload
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run ESLint

## Tech Stack

- **Next.js 14** - React framework
- **React 18** - UI library
- **Material-UI (MUI)** - Component library
- **TypeScript** - Type safety
- **Axios** - HTTP client

## WebSocket Integration

The dashboard connects to the WebSocket server at `ws://localhost:8765` for real-time updates of:
- Arbitrage opportunities
- Trade execution status
- Pool liquidity changes
- System alerts

## Troubleshooting

### Backend Connection Failed

If you see "Failed to connect to backend API":
1. Ensure the backend is running: `cd backend && uvicorn main:app --reload`
2. Check that the backend is accessible at http://localhost:8000
3. Verify CORS settings in backend/main.py

### Installation Errors

If `npm install` fails:
1. Clear npm cache: `npm cache clean --force`
2. Delete `node_modules` and `package-lock.json`
3. Run `npm install` again

## License

MIT
