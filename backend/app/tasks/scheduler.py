import asyncio

from app.db.session import SessionLocal
from app.services.scheduler_service import SchedulerService


async def scheduler_loop():
    print("Scheduler started.")

    while True:
        db = SessionLocal()

        try:
            service = SchedulerService(db)

            processed = await service.process_scheduled_posts()

            if processed:
                print(
                    f"Scheduler processed {processed} post(s)."
                )

        except Exception as exc:
            print(
                f"Scheduler error: {exc}"
            )

        finally:
            db.close()

        await asyncio.sleep(10)