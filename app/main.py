# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str = None):
#     return {"item_id": item_id, "q": q}


from fastapi import FastAPI

from app.database import engine
from app.models import Notification, UserPreference
from app.database import Base
from app.routes.notification_routes import router

app = FastAPI()

# create tables
Base.metadata.create_all(bind=engine)

# Register routes
app.include_router(router)

@app.get("/")
def root():
    return {
        "message": "Notification Service Running"
    }

# @app.get("/notifications")
# def get_notifications():
#     return notification_service.get_all_notifications()


# import threading

# from app.workers.notification_worker import process_notifications


# thread = threading.Thread(
#     target=process_notifications
# )

# thread.daemon = True
# thread.start()

