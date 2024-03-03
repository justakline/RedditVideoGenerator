from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    # Exchange the code for a token...
    # (Make sure to implement the token exchange here)
    return 'Authorization code: ' + code

if __name__ == '__main__':
    app.run(port=8080)