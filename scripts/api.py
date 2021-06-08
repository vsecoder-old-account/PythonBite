import os
import sys
import random
import subprocess

def code_start(code):
	num = random.randint(0, 100000000)
	try:
		f = open(f'test{num}.py', 'w', encoding='utf8')
		f.write(code)
		f.close()
		print(code)
		result = subprocess.run(
			f'python test{num}.py'.split(), 
			stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
			shell=True, check=True, timeout=3
		).stdout.decode('utf-8')
		print(result)
		try:
			os.remove(f'test{num}.py')
		except Exception as e:
			print('File remove error: ' + str(e))
		return result
	except subprocess.CalledProcessError as e:
		print('Subprocess ' + str(e))
		return str(e.output)
	except Exception as e:
		print('Exception ' + str(e))
		return str(e)
