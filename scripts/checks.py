import os
import string
import random
import hashlib
import subprocess
import time
import secrets

from models import db_session
from models.users import User
from models.tests import Test

db_session.global_init('database.db')

def hash_password(password):
	h = hashlib.md5(password.encode())
	return h.hexdigest()

def generate_token():
	token = secrets.token_urlsafe(20)
	return token

def check_token(token):
	session = db_session.create_session()
	user_all = session.query(User).all()

	for user in user_all:
		if (token):
			if str(user.token) == str(token):
				return True

	return False

def create_user(id, email, token, password):
	session = db_session.create_session()
	user = User(
		id=id,
		email=email,
		token=generate_token(),
		hash_password=hash_password(password),
		score=0
	)
	session.add(user)
	session.commit()

def get_user(id):
	session = db_session.create_session()
	user_all = session.query(User).all()

	for user in user_all:
		if (id):
			if str(user.id) == str(id):
				user_as_dict = User(
					id=user.id,
					email=user.email,
					token=user.token,
					hash_password=user.hash_password,
                    score=user.score
				)
				return user_as_dict
		else:
			return

def check_pass(login, password):
	session = db_session.create_session()
	user_all = session.query(User).all()
	users_list = []

	for user in user_all:
		if (login):
			if str(user.email) == str(login):
				if user.hash_password == hash_password(password):
					return user.id
		else:
			break

	print(users_list)
	return users_list

def get_test(id):
	session = db_session.create_session()
	tests = session.query(Test).all()

	for test in tests:
		if (id):
			if str(test.id) == str(id):
				test_as_dict = Test(
					id=test.id,
					name=test.name,
					text=test.text,
					startcode=test.startcode,
					input=test.input,
					output=test.output,
					use=test.use,
					complete=test.complete,
					say=test.say
				)
				return test_as_dict
		else:
			return

def get_tests():
	session = db_session.create_session()
	tests = session.query(Test).all()
	tests_arr = []
	arr = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

	for test in tests:
		test_as_dict = Test(
			id=test.id,
			name=test.name,
            complete=test.complete,
			say=test.say
		)
		tests_arr.append(test_as_dict)
	
	return tests_arr
