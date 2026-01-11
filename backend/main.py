import os
import sys

# Load environment variables BEFORE importing app modules
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import endpoints
from app.core.config import get_logger, get_openai_api_key

# Get logger
logger = get_logger(__name__)


def validate_environment():
    """
    Validate that required environment variables are set.

    This function should be called at application startup to fail fast
    if required configuration is missing.

    Raises:
        SystemExit: If required environment variables are not set
    """
    required_vars = []
    missing_vars = []

    # Check if OPENAI_API_KEY is set
    api_key = get_openai_api_key()
    if not api_key:
        missing_vars.append("OPENAI_API_KEY")
        required_vars.append("OPENAI_API_KEY")

    # Check for OPENAI_API_BASE (optional)
    api_base = os.getenv("OPENAI_API_BASE")
    if api_base:
        logger.info(f"Using custom OpenAI API base: {api_base}")

    if missing_vars:
        logger.error("=" * 80)
        logger.error("FATAL: Required environment variables are not set!")
        logger.error("=" * 80)
        for var in missing_vars:
            logger.error(f"  - {var}")

        logger.error("")
        logger.error("Please set the required environment variables:")
        logger.error("  export OPENAI_API_KEY='your-api-key-here'")
        logger.error("")
        logger.error("Or create a .env file with:")
        logger.error("  OPENAI_API_KEY=your-api-key-here")
        logger.error("=" * 80)
        sys.exit(1)


# Validate environment on import
validate_environment()


app = FastAPI(
    title="PDD Generator API",
    description="AI-powered Process Design Document Generator",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(endpoints.router, tags=["pdd"])


@app.on_event("startup")
async def startup_event():
    """
    Log application startup.
    """
    logger.info("=" * 80)
    logger.info("PDD Generator API starting up...")
    logger.info(f"Version: {app.version}")
    logger.info(f"Documentation available at: http://localhost:8000/docs")
    logger.info("=" * 80)


@app.get("/")
async def root():
    return {
        "message": "PDD Generator API",
        "version": "1.0.0",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
