import boto3
import os
from dotenv import load_dotenv

load_dotenv()


class SNSService:

    def __init__(self):
        self.client = boto3.client(
            "sns",
            region_name=os.getenv("AWS_REGION"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )

    def publish_to_endpoint(self, endpoint_arn: str, message: str):

        response = self.client.publish(
            TargetArn=endpoint_arn,
            Message=message
        )

        return response

    def create_platform_endpoint(self, token: str, platform_arn: str):

        response = self.client.create_platform_endpoint(
            PlatformApplicationArn=platform_arn,
            Token=token
        )

        return response["EndpointArn"]