# coding: utf-8

import os
import sys
import urllib
from os.path import expanduser
import shutil
import subprocess

USER_HOME = expanduser('~')
DIRLIDIDI_HOME = USER_HOME + '/.dirlididi-wrapper'


def setup(user_token):

	print('Baixando dirlididi.py...')	

	if not os.path.exists(DIRLIDIDI_HOME):
    		os.makedirs(DIRLIDIDI_HOME)
	
	shutil.copy('./dirlididi-wrapper.py', DIRLIDIDI_HOME + '/dirlididi-wrapper.py')
	dirlididi_path = os.path.join(DIRLIDIDI_HOME, 'dirlididi.py')
	urllib.urlretrieve('http://dirlididi.com/tools/dirlididi.py', dirlididi_path)
	
	print('Download concluído. Configurando ambiente...')

	with open(USER_HOME + '/.bashrc', 'a') as bashrc:
    		bashrc.write('\nexport DIRLIDIDI_HOME=' + DIRLIDIDI_HOME)
		bashrc.write('\nexport DIRLIDIDI_USER_TOKEN=' + user_token)
		bashrc.write('\nalias dirlididi="python $DIRLIDIDI_HOME/dirlididi-wrapper.py"')

	print('Perfeito. Pronto pra usar =D')

def submit(problem_token, executable_name, source_name):
	user_token = os.environ['DIRLIDIDI_USER_TOKEN']
	dirlididi_path = os.environ['DIRLIDIDI_HOME'] + '/dirlididi.py'
	os.system('bash -c "python %s submit %s %s %s %s"' %
		(dirlididi_path, problem_token, user_token, executable_name, source_name))


def help():
	print('Uso: dirlididi [OPÇÃO]')
	print('Opções')
	print('-i <token> - Instala e configura o dirlididi para submissões feitas com um determinado usuário que possui o token dado.')
	print('-s <prob_token> <exec_file> <source_file> - Submete um código e seu executável para um determinado problema.')
	print('-h - Exibe as opções de uso.')


if __name__ == '__main__':
	if len(sys.argv) > 1:
		option = sys.argv[1]
		if len(sys.argv) == 3 and option == '-i':
			user_token = sys.argv[2]
			setup(user_token)
		elif len(sys.argv) == 4 and option == '-s':
			problem_token = sys.argv[2]
			executable_name = sys.argv[3]
			source_name = sys.argv[4]
			submit(problem_token, executable_name, source_name)
		else:
			help()
	else:
		help()
