#!/usr/bin/env bash
set -e
echo "Booting ZeroDog: AI Behavioral FinOps & MCP Governance Proxy..."
python3 scripts/prebake_seed.py
exec python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
