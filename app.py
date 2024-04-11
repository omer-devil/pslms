from flask import Flask
from settings import Settings
from blueprint.login.login import LOGIN

var = Settings()
var.variables()

app = Flask(__name__)

app.secret_key = var.SECRAT_KEY


app.register_blueprint(LOGIN)

