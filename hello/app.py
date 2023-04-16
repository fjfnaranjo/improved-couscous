from bottle import default_app, route, run


@route("/")
def index():
    return ""


app = default_app()


if __name__ == "__main__":
    run(host="0.0.0.0", port=8080)
