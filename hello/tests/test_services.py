from datetime import datetime
from unittest.mock import MagicMock, patch, sentinel

import pytest

from hello.services import BirthdayService, BirthdayServiceError


@patch("hello.services.boto3")
def test_init(boto3):
    resource_mock = MagicMock()
    boto3.resource.return_value = resource_mock
    service = BirthdayService()
    boto3.resource.assert_called_once_with("dynamodb")
    service.dynamodb.Table.assert_called_once_with("ImprovedCouscous")


@patch("hello.services.boto3")
def test_set_birthday(boto3):
    now = datetime.now()
    now_txt = now.strftime("%Y-%m-%d")
    service = BirthdayService()
    service.set_birthday(sentinel.name, now)
    service.table.put_item.assert_called_once_with(
        Item={"Username": sentinel.name, "Birthday": now_txt}
    )


@patch("hello.services.boto3")
def test_get_birthday(boto3):
    now = datetime.today()
    now_txt = now.strftime("%Y-%m-%d")
    service = BirthdayService()
    service.table.get_item.return_value = {"Item": {"Birthday": now_txt}}
    returned = service.get_birthday(sentinel.name)
    service.table.get_item.assert_called_once_with(
        Key={"Username": sentinel.name},
        ProjectionExpression="Birthday",
    )
    assert returned == datetime.strptime(now_txt, "%Y-%m-%d")


@patch("hello.services.boto3")
def test_get_birthday_not_found(boto3):
    service = BirthdayService()
    service.table.get_item.return_value = {}
    with pytest.raises(BirthdayServiceError):
        service.get_birthday(sentinel.name)
