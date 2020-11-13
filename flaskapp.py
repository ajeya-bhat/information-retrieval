from flask import *
import os
import query
from Elasticsearch.ES import search_snippet


app = Flask(__name__)

@app.route('/')
def home():
    return render_template("search.html")

@app.route('/search', methods = ["POST"])
def submit():
    reqobj = request.json
    print(reqobj)
    if reqobj['engine'] == 1:
        return jsonify(query.main(reqobj['query'])), 200
    elif reqobj['engine'] == 2:
        return jsonify(search_snippet(reqobj['query'])['hits']), 200
    else:
      abort(400)
if __name__ == '__main__':  
    app.run(debug = True, port = 5000, host = "0.0.0.0")
