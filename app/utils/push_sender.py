from app.core.sns_service import SNSService

sns_service = SNSService()


def send_push_notification(endpoint_arn, message):

    try:
        print("Sending PUSH via SNS...")

        response = sns_service.publish_to_endpoint(
            endpoint_arn=endpoint_arn,
            message=message
        )

        print("Push sent successfully:", response)

    except Exception as e:
        print("Push failed:", e)
        raise