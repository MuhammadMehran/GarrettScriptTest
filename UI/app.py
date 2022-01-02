from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('search.html')

@app.route('/search/results', methods=['GET', 'POST'])
def search_request():
    search_term = request.form["input"]

    url = "https://flasktest.proitsquad.com/search2/" + search_term

    payload={}
    headers = {}

    res = requests.request("GET", url, headers=headers, data=payload)



    return render_template('results.html', res=res.json() )
    return jsonify(res.json())
    return render_template('results.html', res=res )

if __name__ == '__main__':
    app.run()