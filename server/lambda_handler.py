from mangum import Mangum

from app import app

handler = Mangum(app)


def lambda_handler(event, context):  # pragma: no cover - lambda entry point
    return handler(event, context)

