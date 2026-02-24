from fastapi import FastAPI
import models
from database import engine
from routers import bus,teacher,scan,authentication,admin
from apscheduler.schedulers.background import BackgroundScheduler
from repository import generatebill
import logging

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s-%(levelname)s-%(message)s"
)

logger=logging.getLogger(__name__)


models.Base.metadata.create_all(engine)
app=FastAPI()
app.include_router(bus.router)
app.include_router(teacher.router)
app.include_router(scan.router)
app.include_router(authentication.router)
app.include_router(admin.router)

scheduler=BackgroundScheduler()
scheduler.add_job(generatebill.bill,'cron',day='1',hour=0,minute=0)
scheduler.start()