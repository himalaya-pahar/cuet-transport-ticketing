import logging
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from database import SessionLocal
import models
from config import settings

logger = logging.getLogger(__name__)


def generate_monthly_bills(db: Session = None, target_date: datetime = None) -> dict:
    """
    Generates monthly transport bills for all active teachers for the preceding month.
    Covers the interval [first_day_of_prev_month, first_day_of_current_month).
    """
    own_session = False
    if db is None:
        db = SessionLocal()
        own_session = True

    try:
        now = target_date or datetime.now(timezone.utc)
        first_day_current_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        last_day_prev_month = first_day_current_month - timedelta(days=1)
        first_day_prev_month = last_day_prev_month.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        billing_month = first_day_prev_month.strftime("%B-%Y")

        logger.info(f"Starting billing generation for {billing_month} ({first_day_prev_month} to {first_day_current_month})")

        teachers = db.query(models.Teacher).filter(models.Teacher.is_active == True).all()
        if not teachers:
            logger.warning("No active teachers found in the database. Skipping bill generation.")
            return {"bills_generated": 0, "billing_month": billing_month, "message": "No active teachers found"}

        bills_count = 0
        fare_per_trip = settings.FARE_PER_TRIP

        for teacher in teachers:
            total_trips = db.query(models.Logs).filter(
                models.Logs.teacher_id == teacher.id,
                models.Logs.time >= first_day_prev_month,
                models.Logs.time < first_day_current_month
            ).count()

            if total_trips > 0:
                total_bill = total_trips * fare_per_trip
                # Check for existing bill to maintain idempotency
                existing_bill = db.query(models.Bill).filter(
                    models.Bill.teacher_id == teacher.id,
                    models.Bill.billing_month == billing_month
                ).first()

                if existing_bill:
                    existing_bill.total_trips = total_trips
                    existing_bill.fare_per_trip = fare_per_trip
                    existing_bill.total_bill = total_bill
                else:
                    new_bill = models.Bill(
                        teacher_id=teacher.id,
                        total_trips=total_trips,
                        fare_per_trip=fare_per_trip,
                        total_bill=total_bill,
                        billing_month=billing_month,
                        status="unpaid"
                    )
                    db.add(new_bill)
                bills_count += 1

        db.commit()
        logger.info(f"Successfully generated/updated {bills_count} bills for {billing_month}")
        return {
            "bills_generated": bills_count,
            "billing_month": billing_month,
            "message": f"Successfully processed {bills_count} bills for {billing_month}"
        }
    except Exception as e:
        db.rollback()
        logger.error(f"Error during bill generation: {e}", exc_info=True)
        raise e
    finally:
        if own_session:
            db.close()


# Legacy alias
def bill():
    generate_monthly_bills()
