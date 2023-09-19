import boto3
import os
import json


def send_message(message: dict):
    try:
        sqs_client = boto3.client(
            "sqs",
            region_name="eu-central-1",
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        )

        queue = sqs_client.get_queue_url(QueueName="msync-sqs-queue-dev-eu-central-1")
        body: str = json.dumps(message)
        response = sqs_client.send_message(
            QueueUrl=queue["QueueUrl"],
            DelaySeconds=10,
            MessageAttributes={
                "Title": {"DataType": "String", "StringValue": "Email"},
            },
            MessageBody=body,
        )
        print(response)
    except Exception as e:
        print("Error in sending message \n{}".format(e))
        return None


# if __name__ == "__main__":
#     send_message(message={"from_email": "admin@poczta.pl"})
