from datetime import datetime

import boto3


class BirthdayServiceError(Exception):
    pass


class BirthdayService:
    def __init__(self):
        self.dynamodb = boto3.resource("dynamodb")
        self.table = self.dynamodb.Table("ImprovedCouscous")

    def set_birthday(self, username, date):
        self.table.put_item(
            Item={
                "Username": username,
                "Birthday": date.strftime("%Y-%m-%d"),
            }
        )

    def get_birthday(self, username):
        try:
            response = self.table.get_item(
                Key={"Username": username},
                ProjectionExpression="Birthday",
            )
        except self.dynamodb.meta.client.exceptions.ResourceNotFoundException as err:
            raise BirthdayServiceError("Birthday not found")
        else:
            return datetime.strptime(response["Item"]["Birthday"], "%Y-%m-%d")
