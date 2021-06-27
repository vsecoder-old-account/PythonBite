from flask import Flask, render_template, flash, redirect, url_for, request, jsonify
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
import os, string, random, time
from scripts.checks import check_token, create_user, get_user, check_pass, get_test, get_tests, get_forums, get_forum, commit_forum, create_forum
from scripts.api import code_start
from memory_profiler import memory_usage

app = Flask(__name__)
app.config['SECRET_KEY'] = 'PythonBite'

login_manager = LoginManager(app)
login_manager.login_view = 'login_page'

@login_manager.user_loader
def load_user(user_id):
    return get_user(user_id)

@app.route("/", methods=['GET', 'POST'])
def index():
	return render_template('index.html')

@app.route("/forum", methods=['GET', 'POST'])
def forums():
	quests = get_forums()
	return render_template('forums.html', quests=quests)

@app.route("/t/create", methods=['GET', 'POST'])
def create():
	return render_template('add_forum.html')

@app.route("/f/<id>", methods=['GET', 'POST'])
def forum(id):
	quest = get_forum(id)
	return render_template('forum.html', quest=quest)

@app.route("/t/commit", methods=['GET', 'POST'])
def forum_com():
	id = random.randint(1000000000, 9999999999)
	name = '' #
	title = ''
	lesson = ''
	quest = ''
	userid = '' #
	if request.method == 'GET':
		name = request.values.get('name')
		title = request.values.get('title')
		lesson = request.values.get('lesson')
		quest = request.values.get('quest')
		userid = request.values.get('userid')
	elif request.method == 'POST':
		name = request.form.get('name')
		title = request.form.get('title')
		lesson = request.form.get('lesson')
		quest = request.form.get('quest')
		userid = request.form.get('userid')

	create_forum(id, name, title, lesson, quest, '', userid)
	return redirect(f"https://pythonbite.herokuapp.com/f/{id}", code=200)

@app.route("/t/add", methods=['GET', 'POST'])
def forum_create():
	id = ''
	id2 = ''
	text = ''
	if request.method == 'GET':
		id = request.values.get('id')
		id2 = request.values.get('userid')
		text = request.values.get('answer')
		name = request.values.get('username')
	elif request.method == 'POST':
		id = request.form.get('id')
		id2 = request.values.get('userid')
		name = request.values.get('username')
		answer = request.form.get('answer')
	
	if id and id2 and text:
		print(1)
		commit_forum(id, id2, text, name)

	return redirect(f"https://pythonbite.herokuapp.com/f/{id}", code=200)

@app.route("/profile/<id>")
@login_required
def get_profile(id):
	user = get_user(id)
	if user and user != [] and id == current_user.id:
		return render_template('profile.html', user=current_user)
	elif user != []:
		return render_template('profile.html', user=user)
	else:
		return render_template('404.html'), 404

@app.route("/privacy-policy", methods=['GET', 'POST'])
def privacy():
	return render_template('privacy-policy.html')

@app.route("/help", methods=['GET', 'POST'])
def help():
	return render_template('help.html')

@app.route("/api", methods=['GET', 'POST'])
def api():
	global num
	code = None
	if request.method == 'GET':
		code = request.values.get('code')
		token = request.values.get('token')
		if code == None:
			return jsonify({'status': 'Code not found'})
		else:
			start_time = time.time()
			checked = code_start(code)
			memory = memory_usage()[0] - 30
			stop_time = time.time() - start_time
			if checked:
				if checked[0] == 'b':
					checked = checked.replace('b\'', '', 1)
					checked = checked[:-1]
				return jsonify({'code': code, 'result': checked[:-1], 'time': stop_time, 'memory': memory, 'status': 'Result returned'})
			else:
				return jsonify({'code': code, 'status': 'Result not returned'})
	elif request.method == 'POST':
		code = request.form.get('code')
		token = request.form.get('token')
		valid_token = check_token(token)
		if code == None:
			return jsonify({'status': 'Code not found'})
		elif valid_token == False:
			return jsonify({'status': 'Invalid token'})
		else:
			start_time = time.time()
			checked = code_start(code)
			memory = memory_usage()[0] - 30
			stop_time = time.time() - start_time
			if checked:
				if checked[0] == 'b':
					checked = checked.replace('b\'', '', 1)
					checked = checked[:-1]
				return jsonify({'code': code, 'result': checked[:-1], 'runtime': stop_time, 'memory': memory, 'status': 'Result returned'})
			else:
				return jsonify({'code': code, 'status': 'Result not returned'})
	else:
		jsonify({'status': 'ERROR 500'})

@app.route('/login', methods=['GET', 'POST'])
def login_page():
	login = request.form.get('user')
	password = request.form.get('pass')

	if login and password:
		user = check_pass(login, password)

		if user:
			user = get_user(user)
			login_user(user)

			return redirect('/')
		else:
			flash('Не верны Логин/Пароль')
	else:
		pass
	return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
	login = request.form.get('user')
	password = request.form.get('pass')
	password2 = request.form.get('pass2')

	if request.method == 'POST':
		if not (login or password or password2):
			flash('Пожалуйста, заполните все поля!')
		elif login == '':
			flash('Пожалуйста, заполните все поля!')
		elif password != password2:
			flash('Пароли не совпадают!')
		else:
			id = random.randint(1000000000, 9999999999)
			create_user(id, login, 0, password)
			return redirect(url_for('login_page'))

	return render_template('register.html')

@app.route('/lesson/<id>', methods=['GET', 'POST'])
def test(id):
	test = get_test(id)
	if test:
		return render_template('lesson.html', test=test)
	else:
		return render_template('pay.html')

@app.route('/lessons', methods=['GET', 'POST'])
def tests():
	tests = get_tests()
	return render_template('lessons.html', tests=list(tests))

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('login_page'))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)
