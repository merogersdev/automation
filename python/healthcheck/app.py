#! /usr/bin/env python3
# Version 1.0

from flask import Flask
from dashboard import dashboard
from api import api

app = Flask(__name__)
app.register_blueprint(dashboard, url_prefix="/")
app.register_blueprint(api, url_prefix="/api/v1/")

if __name__ == "__main__":
    app.run(debug=True)
