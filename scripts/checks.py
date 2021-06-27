import os
import string
import random
import hashlib
import subprocess
import time
import json
import secrets

from models import db_session
from models.users import User
from models.tests import Test
from models.forums import Forum

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
		name="Живой динозавр №" + str(id),
		email=email,
		token=generate_token(),
		hash_password=hash_password(password),
		rang=0,
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
					name=user.name,
					email=user.email,
					token=user.token,
					hash_password=user.hash_password,
                    score=user.score,
                    rang=0
				)
				return user_as_dict
		else:
			return

def create_forum(id, name, title, lesson, quest, result, userid):
	session = db_session.create_session()
	forum = Forum(
        id=id,
        name=name,
        title=title,
        lesson=lesson,
        quest=quest,
        results='[{}]',
        user=userid
	)
	session.add(forum)
	session.commit()


def commit_forum(id, id2, answer, name):
	session = db_session.create_session()
	forum_all = session.query(Forum).all()

	for forum in forum_all:
		if (id):
			if str(forum.id) == str(id):
				results = json.loads(forum.results)
				res = {
					'id': id2,
					'name': name,
					'answer': answer
				}
				print(res)
				results.append(res)
				print(results)
				forum.results = str(json.dumps(results))

	session.commit()

def get_forum(id):
	session = db_session.create_session()
	forum_all = session.query(Forum).all()

	for forum in forum_all:
		if (id):
			if str(forum.id) == str(id):
				forum_as_dict = Forum(
					id=forum.id,
					name=forum.name,
					title=forum.title,
					lesson=forum.lesson,
					quest=forum.quest,
					results=json.loads(forum.results),
					user=forum.user
				)
				return forum_as_dict
		else:
			return

def get_forums():
	session = db_session.create_session()
	forum_all = session.query(Forum).all()
	num = 0
	forum_list = []

	for forum in forum_all:
		forum_as_dict = {
			'id': forum.id,
			'name': forum.name,
			'title': forum.title,
			'lesson': forum.lesson,
			'quest': forum.quest,
			'results': len(json.loads(forum.results)),
			'user': forum.user
		}
		forum_list.append(forum_as_dict)

	num = len(forum_list) - 1
	a = 0
	new_list = []

	for i in range(0, 10):
		if a > num:
			return new_list
		new_list.append(forum_list[num-i])
		a += 1

	return new_list

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

	for test in tests:
		test_as_dict = Test(
			id=test.id,
			name=test.name,
            complete=test.complete,
			say=test.say
		)
		tests_arr.append(test_as_dict)
	
	return tests_arr
