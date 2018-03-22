# coding: utf-8

import os
import sys
import urllib
import argparse
from os.path import expanduser
import shutil


USER_HOME = expanduser('~')
DIRLIDIDI_HOME = USER_HOME + '/.dirlididi-wrapper'

def dirlididi_path(filename):
    if not os.path.exists(DIRLIDIDI_HOME):
        os.makedirs(DIRLIDIDI_HOME)
    return os.path.join(DIRLIDIDI_HOME, filename)


def update():
    print('Atualizando dirlididi...')
    path = dirlididi_path('dirlididi.py')
    if os.path.exists(path):
        os.remove(path)
    urllib.urlretrieve('http://dirlididi.com/tools/dirlididi.py', path)
    path = dirlididi_path('dirlididi-wrapper.py')
    if os.path.exists(path):
        os.remove(path)
    urllib.urlretrieve('https://raw.githubusercontent.com/JoseRenan/dirlididi-wrapper/master/dirlididi-wrapper.py', path)
    print('Atualizanção concluída.')


def setup(user_token=None):
    print('Baixando dirlididi.py...')

    path = dirlididi_path('dirlididi.py')
    shutil.copy('./dirlididi-wrapper.py', DIRLIDIDI_HOME + '/dirlididi-wrapper.py')
    urllib.urlretrieve('http://dirlididi.com/tools/dirlididi.py', path)

    print('Download concluído. Configurando ambiente...')

    #if os.environ.get('DIRLIDIDI_HOME') != None:   #impedia de atualizar o user_token
    if (user_token == None):
        print('Perfeito. Pronto pra usar =D')
    else:
        bash_input = []
        with open(USER_HOME + '/.bashrc', "r") as bashrc_in:        # apaga as variaveis
            bash_input = bashrc_in.readlines()

        with open(USER_HOME + '/.bashrc', "w") as bashrc_out:
            for line in bash_input:
                if line[0] == '#':
                    bashrc_out.write(line)
                elif not (("DIRLIDIDI_HOME" in line) or
                    ("DIRLIDIDI_USER_TOKEN" in line) or
                    ("alias dirlididi" in line)):
                    bashrc_out.write(line)

        with open(USER_HOME + '/.bashrc', 'a') as bashrc:
            bashrc.write('\nexport DIRLIDIDI_HOME=' + DIRLIDIDI_HOME)
            bashrc.write('\nexport DIRLIDIDI_USER_TOKEN=' + user_token)
            bashrc.write('\nalias dirlididi="python $DIRLIDIDI_HOME/dirlididi-wrapper.py"')
        print('Perfeito. Por favor, refaça o login no sistema antes de usar =D')

def submit(problem_token, executable_name, source_name):
    user_token = os.environ['DIRLIDIDI_USER_TOKEN']
    path = os.environ['DIRLIDIDI_HOME'] + '/dirlididi.py'
    os.system('bash -c "python %s submit %s %s %s %s"' %
        (path, problem_token, user_token, executable_name, source_name))


def compile_cpp(filename):
    os.system('bash -c "gcc %s.cpp -o %s"' %(filename, filename))

def compile_hs(filename):
    os.system('bash -c "ghc %s.hs -o %s"' %(filename, filename))
    os.system('bash -c "rm %s.o"' %(filename))
    os.system('bash -c "rm %s.hi"' %(filename))

def identify_and_compile(filename):
    sep = filename.rfind('.')
    type_file = filename[sep+1:]
    executable = filename[:sep]
    if type_file == 'cpp':
        compile_cpp(executable)
        return executable
    elif type_file == 'hs':
        compile_hs(executable)
        return executable
    else:
        return ''

def autodetect_and_submit(problem_token, filename):
    executable_name = identify_and_compile(filename)
    submit(problem_token, executable_name, filename)


def get_parser():
    parser = argparse.ArgumentParser(description='Uma CLI wrapper para auxiliar no uso da ferramenta dirlididi.')
    parser.add_argument('-i', help='(Re)instala e configura o dirlididi para submissões feitas com um determinado usuário que possui o token dado.', const='', nargs='?')
    parser.add_argument('-u', help='Atualiza o dirlididi-wrapper para a ultima versão.',)
    parser.add_argument('-s', help='<prob_token> <exec_file> <source_file> - Submete um código e seu executável para um determinado problema.',nargs=3)
    parser.add_argument('-c', help='<prob_token> <source_file> - Submete um código e seu executável para um determinado problema.',nargs=2)
    parser.add_argument('-h', help='Exibe as opções de uso.', default='',)

def help():
    print('Uso: dirlididi [OPÇÃO]')
    print('Opções')
    print('-i <token> - (Re)instala e configura o dirlididi para submissões feitas com um determinado usuário que possui o token dado.')
    print('-i - Recarrega os arquivos sem alterar o token de usuario')
    print('-u - Atualiza o dirlididi-wrapper para a ultima versão.')
    print('-s <prob_token> <exec_file> <source_file> - Submete um código e seu executável para um determinado problema.')
    print('-c <source_file> - Identifica a linguagem pelo formato do arquivo e compila automaticamente.')
    print('-cs <prob_token> <source_file> - Compila automaticamente e submete o arquivo')
    print('-h - Exibe as opções de uso.')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        option = sys.argv[1]
        if len(sys.argv) == 3 and option == '-i':
            user_token = sys.argv[2]
            setup(user_token)

        elif len(sys.argv) == 2 and option == '-i':
            setup()

        elif len(sys.argv) == 2 and option == '-u':
            update()

        elif len(sys.argv) == 5 and option == '-s':
            problem_token = sys.argv[2]
            executable_name = sys.argv[3]
            source_name = sys.argv[4]
            submit(problem_token, executable_name, source_name)

        elif len(sys.argv) == 4 and option == '-s':
            problem_token = sys.argv[2]
            executable_name = sys.argv[3]
            submit(problem_token, executable_name, '')

        elif len(sys.argv) == 3 and option == '-c':
            source_name = sys.argv[2]
            identify_and_compile(source_name)

        elif len(sys.argv) == 4 and option == '-cs':
            problem_token = sys.argv[2]
            source_name = sys.argv[3]
            autodetect_and_submit(problem_token, source_name)

        else:
            help()
    else:
        help()
