import os

from dotenv import load_dotenv
import uvicorn

load_dotenv()

from app import app  # noqa: E402


def run() -> None:
    port = int(os.getenv("PORT", "5000"))
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    run()
