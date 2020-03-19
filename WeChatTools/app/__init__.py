# -*- coding=utf-8 -*-
# python35

from flask import Flask

app = Flask(__name__)
from app import routes
