import os

from flask import Flask, request

from InterfaseDBGame import WorkWithDB

app = Flask(__name__)
db = WorkWithDB({
		"dbname":"sdbgDB",
		"user":"admin",
		"password" : "147753",
		"host":"localhost"
		})


@app.route('/signup', methods=["POST"])
def signup():
	if request.method == "POST":
		login = request.form["login"]
		password = request.form["password"]

		return str(db.signup_in_game(login, password))

@app.route('/signin', methods=["POST"])
def signin():
	if request.method == "POST":
		login = request.form["login"]
		password = request.form["password"]

		return str(db.check_log_and_pass_user(login, password))

@app.route('/update_score', methods=["POST"])
def update_score():
	if request.method == "POST":
		login = request.form["login"]
		score_user = request.form["score_user"]
		number_level = request.form["number_level"]
		db.update_score(login, score_user, number_level)
		return ""

@app.route('/prevate_score', methods=["POST"])
def prevate_score():
	if request.method == "POST":
		login = request.form["login"]
		number_level = request.form["number_level"]

		return str(db.prevate_score(login, number_level))

@app.route('/select_top_10', methods=["POST"])
def select_top_10():
	if request.method == "POST":
		number_level = request.form["number_level"]

		return str(db.select_top_10(number_level))

if __name__ == '__main__':
    # PORT = int(os.environ.get('PORT'))
    app.run(host="localhost", port=5000, debug=True)

