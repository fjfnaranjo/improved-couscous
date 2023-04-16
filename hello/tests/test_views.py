from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch, sentinel

from hello.services import BirthdayServiceError
from hello.views import get_request, index, put_request


class ServiceMock:
    def __init__(self):
        self.data = {}

    def get_birthday(self, username):
        if username not in self.data:
            raise BirthdayServiceError
        else:
            return datetime.strptime(self.data[username], "%Y-%m-%d")

    def set_birthday(self, username, date):
        self.data[username] = date.strftime("%Y-%m-%d")


def test_index():
    assert index() == ""


@patch("hello.views.response")
def test_get_birthday_dont_exists(response):
    service_mock = ServiceMock()
    get_request(service_mock, sentinel.dont_exists)
    assert response.status == 404


@patch("hello.views.datetime")
@patch("hello.views.response")
def test_get_birthday_yesterday(response, datetime_mock):
    now = datetime.now()
    today = datetime.strptime(now.strftime("%Y-%m-%d"), "%Y-%m-%d")
    datetime_mock.now.return_value = now
    datetime_mock.strptime.return_value = today
    yesterday = now - timedelta(days=1)
    yesterday_day = yesterday.strftime("%Y-%m-%d")
    service_mock = ServiceMock()
    service_mock.data[sentinel.yesterday] = yesterday_day
    returned = get_request(service_mock, sentinel.yesterday)
    assert "was 1 day(s) ago" in returned


@patch("hello.views.datetime")
@patch("hello.views.response")
def test_get_birthday_today(response, datetime_mock):
    now = datetime.now()
    today = datetime.strptime(now.strftime("%Y-%m-%d"), "%Y-%m-%d")
    datetime_mock.now.return_value = now
    datetime_mock.strptime.return_value = today
    today_day = today.strftime("%Y-%m-%d")
    service_mock = ServiceMock()
    service_mock.data[sentinel.today] = today_day
    returned = get_request(service_mock, sentinel.today)
    assert "Happy" in returned


@patch("hello.views.datetime")
@patch("hello.views.response")
def test_get_birthday_tomorrow(response, datetime_mock):
    now = datetime.now()
    today = datetime.strptime(now.strftime("%Y-%m-%d"), "%Y-%m-%d")
    datetime_mock.now.return_value = now
    datetime_mock.strptime.return_value = today
    tomorrow = now + timedelta(days=1)
    tomorrow_day = tomorrow.strftime("%Y-%m-%d")
    service_mock = ServiceMock()
    service_mock.data[sentinel.tomorrow] = tomorrow_day
    returned = get_request(service_mock, sentinel.tomorrow)
    assert "is in 1 day(s)" in returned


@patch("hello.views.response")
@patch("hello.views.request")
def test_set_birthday_not_json(request, response):
    service_mock = ServiceMock()
    request.json.side_effect = ValueError
    put_request(service_mock, sentinel.new)
    assert response.status == 400


@patch("hello.views.response")
@patch("hello.views.request")
def test_set_birthday_missing_date(request, response):
    service_mock = ServiceMock()
    request.json = {}
    put_request(service_mock, sentinel.new)
    assert response.status == 400


@patch("hello.views.datetime")
@patch("hello.views.response")
@patch("hello.views.request")
def test_set_birthday_not_a_date(request, response, datetime_mock):
    service_mock = ServiceMock()
    request.json = {"dateOfBirth": "not-a-date"}
    datetime_mock.strptime.side_effect = ValueError
    put_request(service_mock, sentinel.new)
    assert response.status == 400


@patch("hello.views.datetime")
@patch("hello.views.response")
@patch("hello.views.request")
def test_set_birthday_yesterday(request, response, datetime_mock):
    now = datetime.now()
    today_day = datetime.strptime(now.strftime("%Y-%m-%d"), "%Y-%m-%d")
    datetime_mock.now.return_value = now
    yesterday = datetime.now() - timedelta(days=2)
    yesterday_text = yesterday.strftime("%Y-%m-%d")
    yesterday_day = datetime.strptime(yesterday_text, "%Y-%m-%d")
    service_mock = ServiceMock()
    request.json = {"dateOfBirth": yesterday_text}
    datetime_mock.strptime.side_effect = [
        yesterday_day,
        today_day,
    ]
    put_request(service_mock, sentinel.new)
    assert response.status == 400


@patch("hello.views.datetime")
@patch("hello.views.response")
@patch("hello.views.request")
def test_set_birthday_tomorrow(request, response, datetime_mock):
    now = datetime.now()
    today_day = datetime.strptime(now.strftime("%Y-%m-%d"), "%Y-%m-%d")
    datetime_mock.now.return_value = now
    tomorrow = datetime.now() + timedelta(days=2)
    tomorrow_text = tomorrow.strftime("%Y-%m-%d")
    tomorrow_day = datetime.strptime(tomorrow_text, "%Y-%m-%d")
    service_mock = ServiceMock()
    request.json = {"dateOfBirth": tomorrow_text}
    datetime_mock.strptime.side_effect = [
        tomorrow_day,
        today_day,
    ]
    put_request(service_mock, sentinel.new)
    assert response.status == 204
    assert service_mock.data[sentinel.new] == tomorrow_text
