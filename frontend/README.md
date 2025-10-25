# Billionaire Arbitrage System - Frontend

Next.js-based dashboard for monitoring and executing arbitrage opportunities.

## Getting Started

### Install Dependencies

```bash
npm install
```

### Run Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build for Production

```bash
npm run build
npm start
```

## Features

- Real-time system status monitoring
- Live pool data visualization
- Opportunity detection and execution
- Material-UI components
- Dark theme optimized for trading

## Configuration

The frontend connects to the backend API at `http://localhost:8000` by default.
Modify `next.config.js` to change the API endpoint.

## Structure

- `src/pages/` - Next.js pages
- `src/components/` - React components
- `public/` - Static assets
