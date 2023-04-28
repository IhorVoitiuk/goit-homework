"""
This module defines the main FastAPI application for the project.

The application includes middleware for measuring performance and handling CORS requests,
as well as routes for user authentication, user management, and contact management.

Additionally, the module includes startup logic for initializing a Redis instance and a
database connection pool, and a healthchecker endpoint for verifying the application's
connection to the database.

Dependencies:
- fastapi
- fastapi_limiter
- sqlalchemy
- redis
- uvicorn

Usage:
    Run the module directly to start the application server.
"""

import time
import redis.asyncio as redis

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from sqlalchemy.orm import Session
from sqlalchemy import text

from src.database.db import get_db
from src.routes import contacts, auth, users
from src.conf.config import settings

app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    r = await redis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=0,
        encoding="utf-8",
        decode_responses=True,
    )
    await FastAPILimiter.init(r)


@app.middleware("http")
async def custom_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    during = time.time() - start_time
    response.headers["performance"] = str(during)
    return response


@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        # Make request
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database is not configured correctly",
            )
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error connecting to the database",
        )


@app.get("/")
def main_pange():
    return {"greating": "Hello FastAPI"}


app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(contacts.router, prefix="/api")


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
