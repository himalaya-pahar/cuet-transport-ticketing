import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler

import models
from database import engine
from config import settings
from routers import bus, teacher, scan, authentication, admin, bill
from repository import generatebill

# Configure logging
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup sequence
    logger.info("Starting up application...")
    models.Base.metadata.create_all(engine)
    scheduler.add_job(generatebill.generate_monthly_bills, 'cron', day='1', hour=0, minute=0)
    scheduler.start()
    logger.info("APScheduler initialized and running.")
    yield
    # Shutdown sequence
    logger.info("Shutting down application...")
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("APScheduler stopped.")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Automated Transport Ticketing and Monthly Billing System for Chittagong University of Engineering and Technology (CUET).",
    lifespan=lifespan
)

# CORS Middleware for Web & Mobile Clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(authentication.router)
app.include_router(admin.router)
app.include_router(teacher.router)
app.include_router(bus.router)
app.include_router(scan.router)
app.include_router(bill.router)


@app.get("/", tags=["Health"])
def health_check():
    return {
        "status": "online",
        "service": settings.PROJECT_NAME,
        "docs_url": "/docs"
    }