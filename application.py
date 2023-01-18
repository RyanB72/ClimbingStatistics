from flask import Flask, render_template, request
import json
from datetime import datetime
from collections import Counter

application = Flask(__name__)

@application.route('/')
def index():
    #today = datetime.now().strftime("%Y-%m-%d")
    return 'does this fix it somehow'

if __name__ == '__main__':
    application.run()