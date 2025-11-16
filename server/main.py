"""Local development entry point for running the FastAPI app."""

import os

import uvicorn
from dotenv import load_dotenv

load_dotenv()

from app import app  # noqa: E402


def run() -> None:
    """Start uvicorn using the configured FastAPI app."""
    port = int(os.getenv('PORT', '5000'))
    uvicorn.run(app, host='127.0.0.1', port=port)


if __name__ == '__main__':
    run()
