from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from .api.v1.api import router as api_router
from .core.config import settings
from .database import engine, Base
from .core.config import settings
from pathlib import Path

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run on startup
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    # Create upload directory
    Path(settings.UPLOAD_DIR).mkdir(exist_ok=True)
    print("Initialization complete!")
    
    yield  # The application runs here
    
    # Code to run on shutdown (optional)
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router, prefix="/api/v1")
