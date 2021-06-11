from flask import Flask, render_template, flash, redirect, url_for, request, jsonify
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
import os, string, random, hashlib, subprocess, time, secrets
from scripts.checks import check_token, create_user, get_user, check_pass, get_test, get_tests
from scripts.api import code_start
from memory_profiler import memory_usage

app = Flask(__name__)
app.config['SECRET_KEY'] = 'api'

login_manager = LoginManager(app)
login_manager.login_view = 'login_page'

@login_manager.user_loader
def load_user(user_id):
    return get_user(user_id)

@app.route("/", methods=['GET', 'POST'])
def index():
	return render_template('index.html')

@app.route("/profile/<id>")
@login_required
def get_profile(id):
	user = get_user(id)
	if user != [] and id == current_user.id:
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
				return jsonify({'code': code, 'result': checked[:-2], 'time': stop_time, 'memory': memory, 'status': 'Result returned'})
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
				return jsonify({'code': code, 'result': checked[:-2], 'runtime': stop_time, 'memory': memory, 'status': 'Result returned'})
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
	return render_template('lesson.html', test=test)

@app.route('/lessons', methods=['GET', 'POST'])
def tests():
	tests = get_tests()
	return render_template('lessons.html', tests=list(reversed(tests)))

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
