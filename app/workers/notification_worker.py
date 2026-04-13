import time

from app.database import SessionLocal
from app.models import Notification
from sqlalchemy import case


def process_notifications():
    db = SessionLocal()

    while True:

        print("Checking for pending notifications...")
        priority_order = case(
            (Notification.priority == "high", 1),
            (Notification.priority == "medium", 2),
            (Notification.priority == "low", 3),
        )

        notifications = (
            db.query(Notification)
            .filter(Notification.status == "pending")
            .order_by(priority_order)
            .all()
        )

        for n in notifications:
                
            try:
                print(
                    f"Processing ID={n.id}, "
                    f"Priority={n.priority}, "
                    f"Message={n.message}"
                )

                # Simulate failure
                if n.message == "FAIL":
                    raise Exception("Simulated failure")

                n.status = "sent"

            except Exception as e:

                n.retry_count += 1

                print(
                    f"Retry {n.retry_count} "
                    f"for ID={n.id}"
                )

                if n.retry_count >= 3:
                    n.status = "failed"
                    print(
                        f"Notification {n.id} FAILED"
                    )


        db.commit()

        time.sleep(5)