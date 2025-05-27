from flask import Flask, request, render_template, redirect,jsonify, Response
import requests
import os

app = Flask(__name__)
webpath = os.path.join(os.getcwd(),'webhuntedwebsite.html')

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method== 'POST':
        pass
    else:
        return render_template('webhunter.html')
@app.route('/website', methods=['GET'])
def website():
    website_url = request.args.get('search')
    if not website_url.startswith('http'):
        website_url = 'https://'+ website_url
    webhunter = requests.get(website_url)
    if webhunter.status_code>=400:
        return jsonify({"Error": webhunter.status_code})
    else:
        return webhunter.text
@app.route('/html', methods=['GET'])
def html():
    website_url = request.args.get('search')
    if not website_url.startswith('http'):
        website_url = 'https://'+ website_url
    webhunter = requests.get(website_url)
    if webhunter.status_code>=400:
        return jsonify({"Error": webhunter.status_code})
    else:
        with open(webpath, 'w') as file:
            file.write(webhunter.text)
            return Response(webhunter.text, mimetype='text/plain')

    

if __name__ == '__main__':
    app.run(debug=True)