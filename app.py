import os


from flask import Flask, request, Response

from InterfaseUserGame import WorkWithUser
from Session import WorkWithSession

app = Flask(__name__)
user = WorkWithUser()
session = WorkWithSession(os.environ.get('KEY_GENERATION'))

# decorator check session to existens
def dec_check_session(func): 
	def wrapper(*args, **kwargs):
		key = request.headers.get("Key-session-client")
		if session.check_session(key):
			return func()
		else:
			return "Wrong key!!!"
	wrapper.__name__ = func.__name__
	return wrapper

@app.route('/signup', methods=["POST"])
def signup():
	if request.method == "POST":
		login = request.form["login"]
		password = request.form["password"]

		return str(user.signup_in_game(login, password))
 
@app.route('/signin', methods=["POST"])
def signin():
	if request.method == "POST":
		login = request.form["login"]
		password = request.form["password"]
		if user.signin_in_game(login, password):
			resp = Response("True")
			resp.headers['Key-session-server'] = session.create_session()
			return resp
		else:
			return False

@app.route('/update_score', methods=["POST"])
@dec_check_session
def update_score():
	if request.method == "POST":
		login = request.form["login"]
		score_user = request.form["score_user"]
		number_level = request.form["number_level"]
		user.update_score(login, score_user, number_level)

		return ""

@app.route('/prevate_score', methods=["POST"])
@dec_check_session
def prevate_score():
	if request.method == "POST":
		login = request.form["login"]
		number_level = request.form["number_level"]

		return str(user.prevate_score(login, number_level))

@app.route('/select_top_10', methods=["POST"])
@dec_check_session
def select_top_10():
	if request.method == "POST":
		number_level = request.form["number_level"]

		return str(user.select_top_10(number_level))

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT'))
    app.run(host="0.0.0.0.0", port=PORT)

