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


def setup(user_token):
    print('Baixando dirlididi.py...')

    path = dirlididi_path('dirlididi.py')
    shutil.copy('./dirlididi-wrapper.py', DIRLIDIDI_HOME + '/dirlididi-wrapper.py')
    urllib.urlretrieve('http://dirlididi.com/tools/dirlididi.py', path)

    print('Download concluído. Configurando ambiente...')

    #if os.environ.get('DIRLIDIDI_HOME') != None:   #impedia de atualizar o user_token
    if (user_token == ' '):
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
    parser.add_argument('-i', help='(Re)instala e configura o dirlididi para submissoes feitas com um determinado usuario que possui o token dado.' + 
        'Caso nao seja informado o token, ira recarregar os arquivos sem alterar o token de usuario', const=' ', nargs='?', metavar='<token>')
    parser.add_argument('-u', help='Atualiza o dirlididi-wrapper para a ultima versao.', action='store_true')
    parser.add_argument('-s', help='Submete um codigo e seu executavel para um determinado problema.', 
        nargs=3, metavar=('<prob_token>', '<exec_file>', '<source_file>'))
    parser.add_argument('-c', help='Identifica a linguagem pelo formato do arquivo e compila automaticamente.', nargs=1, metavar='<source_file>')
    parser.add_argument('-cs', help='Compila automaticamente e submete o arquivo', nargs=2, metavar=('<prob_token>', '<source_file>'))
    return parser


def command_line_runner():
    parser = get_parser()
    args = vars(parser.parse_args())

    if(args['i']):
        user_token = args['i']
        setup(user_token)

    elif(args['u']):
        update()
    
    elif(args['s']):
        problem_token, executable_name, source_name = args['s']
        submit(problem_token, executable_name, source_name)
    
    elif(args['c']):
        source_name = args['c'][0]
        identify_and_compile(source_name)
    
    elif(args['cs']):
        problem_token, source_name = args['cs']
        autodetect_and_submit(problem_token, source_name)
    
    else:
        parser.print_help()


    

if __name__ == '__main__':
    command_line_runner()




