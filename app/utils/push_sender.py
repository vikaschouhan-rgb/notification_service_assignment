import logging
from app.core.sns_service import SNSService

sns_service = SNSService()
logger = logging.getLogger(__name__)


def send_push_notification(endpoint_arn, message):
    try:
        logger.info(f"Preparing PUSH notification for endpoint={endpoint_arn}")

        logger.info("Sending PUSH via SNS...")

        response = sns_service.publish_to_endpoint(
            endpoint_arn=endpoint_arn,
            message=message
        )

        logger.info(
            f"Push sent successfully to endpoint={endpoint_arn}, "
            f"message_id={response.get('MessageId', 'N/A')}"
        )

        return response

    except Exception as e:
        logger.error(
            f"Push notification failed for endpoint={endpoint_arn}: {str(e)}",
            exc_info=True
        )
        raise
