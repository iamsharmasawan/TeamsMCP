#!/usr/bin/env bash
set -e


# activate venv manually or use your environment
# python -m venv .venv
# source .venv/bin/activate


pip install -r requirements.txt


export $(cat .env | xargs)
python teams_mcp.py