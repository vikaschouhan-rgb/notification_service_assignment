from rq import Queue
from app.core.redis_client import redis_conn

notification_queue = Queue(
    "notifications",
    connection=redis_conn
)