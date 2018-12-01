from os import chdir
from subprocess import call


for chapter in range(1, 13):
    if chapter < 10:
        ch = '0{}'.format(chapter)
    else:
        ch = '{}'.format(chapter)
    chdir('code-ch{}'.format(ch))
    call('nosetests --with-doctest *.py', shell=True)
    chdir('..')
