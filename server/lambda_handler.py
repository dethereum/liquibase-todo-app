"""AWS Lambda entry point that wraps the FastAPI app."""

from mangum import Mangum

from app import app

handler = Mangum(app)


def lambda_handler(event, context):  # pragma: no cover - lambda entry point
    """Forward Lambda invoke events to the ASGI handler."""
    return handler(event, context)
