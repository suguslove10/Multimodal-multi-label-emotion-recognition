#!/bin/bash

echo "🚀 Starting Frontend..."

cd frontend

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📥 Installing frontend dependencies..."
    npm install
fi

# Start Next.js dev server
echo "✅ Starting Next.js on http://localhost:3000"
npm run dev
