import sys
import pathlib
import asyncio

# Ensure todo_app/ is on the Python path
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

import uvicorn
from fastapi import FastAPI

from web_fractal.db import Base
from app.config import HOST, PORT
from app.archtool_conf.bundle_project import bundle

app = FastAPI(title="ToDo Service", version="1.0.0")
_, engine = bundle(app)


@app.on_event("startup")
async def startup() -> None:
    """Create all tables on startup (idempotent)."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    uvicorn.run("run:app", host=HOST, port=PORT, reload=False)
