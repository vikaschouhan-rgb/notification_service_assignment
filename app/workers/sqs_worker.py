import json
import boto3
import os
from dotenv import load_dotenv

from app.utils.push_sender import send_push_notification

load_dotenv()


def poll_sqs():

    sqs = boto3.client(
        "sqs",
        region_name=os.getenv("AWS_REGION"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    queue_url = os.getenv("SQS_QUEUE_URL")

    while True:
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=10
        )

        messages = response.get("Messages", [])

        for msg in messages:
            body = json.loads(msg["Body"])

            print("Received from SQS:", body)

            send_push_notification(
                body["recipient"],
                body["message"]
            )

            # delete after processing
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=msg["ReceiptHandle"]
            )