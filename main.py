"""SignBridge Root Application Entry Point."""
from backend.app.main import app

if __name__ == "__main__":
    import uvicorn
    from backend.app.config import get_settings
    settings = get_settings()
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
