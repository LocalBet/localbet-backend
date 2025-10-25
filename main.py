"""
Start application module.
"""

from uvicorn import run

from backend import Settings

if __name__ == "__main__":
    run(
        app="backend:app",
        host=Settings.APPLICATION_HOST,
        port=Settings.APPLICATION_PORT,
        log_level=Settings.LOG_LEVEL.lower(),
        reload=True,
        reload_delay=2,
    )
