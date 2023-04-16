from datetime import datetime
from json import dumps, loads

from bottle import response, request

from hello.services import BirthdayServiceError


def index():
    return ""


def put_request(birthday_service, username):
    try:
        data = request.json
    except:
        response.status = 400
    else:
        if not "dateOfBirth" in data:
            response.status = 400
        else:
            try:
                date_of_birth = datetime.strptime(data["dateOfBirth"], "%Y-%m-%d")
            except:
                response.status = 400
            else:
                now = datetime.now()
                today = datetime.strptime(now.strftime("%Y-%m-%d"), "%Y-%m-%d")
                if today > date_of_birth:
                    response.status = 400
                else:
                    birthday_service.set_birthday(username, date_of_birth)
                    response.status = 204


def get_request(birthday_service, username):
    try:
        birthday = birthday_service.get_birthday(username)
    except BirthdayServiceError as e:
        response.status = 404
    else:
        now = datetime.now()
        today = datetime.strptime(now.strftime("%Y-%m-%d"), "%Y-%m-%d")
        today_txt = today.strftime("%Y-%m-%d")
        birthday_txt = birthday.strftime("%Y-%m-%d")
        if today == birthday:
            response.headers["Content-Type"] = "application/json"
            return dumps({"message": f"Hello {username}! Happy birthday!"})
        elif today < birthday:
            remaining = birthday - today
            remaining_days = remaining.days
            response.headers["Content-Type"] = "application/json"
            return dumps(
                {
                    "message": f"Hello {username}! Your birthday is in {remaining_days} day(s)"
                }
            )
        else:
            remaining = today - birthday
            remaining_days = remaining.days
            response.headers["Content-Type"] = "application/json"
            return dumps(
                {
                    "message": f"Hello {username}! Your birthday was {remaining_days} day(s) ago"
                }
            )
