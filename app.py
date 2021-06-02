import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from selenium.webdriver.chrome.options import Options
import os
from flask import Flask, Response
from selenium import webdriver
from graphene import ObjectType, String, Schema


class Query(ObjectType):
    # this defines a Field `hello` in our Schema with a single Argument `name`
    hello = String(name=String(default_value="stranger"))
    goodbye = String()

    def resolve_hello(root, info, name):
        return f'Hello {name}!'

    def resolve_goodbye(root, info):
        return 'See ya!'


schema = Schema(query=Query)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.getcwd()}/posts.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


def parse_pages():
    chrome_options = Options()
    chrome_options.add_argument('--verbose')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    browser = webdriver.Remote(
        command_executor='http://localhost:53645/',
        desired_capabilities=chrome_options.to_capabilities())
    browser = webdriver.Chrome()
    # browser.get('http://www.znaj.ua')
    # Titles = browser.find_elements_by_tag_name('h4')
    # for title in Titles:
    #     print(title.text, '\n')
    query_string = '{ hello }'
    result = schema.execute(query_string)
    return Response(query_string)


@app.route("/")
def hello():
    # parsing result
    start_parser_service()
    return parse_pages()


def start_parser_service():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=parse_pages, trigger="interval", seconds=10)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
