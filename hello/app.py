from functools import partial

from bottle import default_app, get, put, run

from hello.services import BirthdayService
from hello.views import put_request, get_request, index


def bootstrap_api():
    birthday_service = BirthdayService()
    get("/")(index)
    put("/hello/<username:re:[a-zA-Z]+>")(partial(put_request, birthday_service))
    get("/hello/<username:re:[a-zA-Z]+>")(partial(get_request, birthday_service))
    return default_app()


app = bootstrap_api()


if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8080)
