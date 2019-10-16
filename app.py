from flask import Flask
import InterfaseDBGame as db
import os
app = Flask(__name__)

@app.route('/<int:rrr>')
def hello_world(rrr):
    return str(rrr+100)

@app.route('/sing_up', methods=['POST'])
def sing_up_in_game():
    ret = request.json
    return get_login_in_DB(ret["login"],ret["password"])


@app.route('/sing_up',methods=['POST'])
def login_up_in_game():
    ret = request.json
    return get_login_in_DB(ret["login"],ret["password"])

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT'))
    app.run(host = "0.0.0.0",port = PORT)
