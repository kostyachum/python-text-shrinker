from flask import Flask, render_template
from flask import request

from texter import Texter, ANALYZE_OPTIONS

app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def index():
    texter = None

    if request.method == 'POST':
        texter = Texter(source_text=request.form['source_text'], analyze_type=request.form['analyze_type'])
        texter.analyze_entities()

    return render_template('index.html', texter=texter, analyze_options=ANALYZE_OPTIONS)
