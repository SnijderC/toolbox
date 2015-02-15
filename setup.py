# -*- coding: utf-8 -*-
import subprocess
import os, shlex, time
import settings
'''
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.MD')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='bof-toolbox',
    version='0.9',
    packages=['toolbox'],
    include_package_data=True,
    license='CCBy-sa 4.0',
    description='BOF Toolbox',
    long_description=README,
    url='https://toolbox.bof.nl',
    author='Chris Snijder',
    author_email='chrissnijder@me.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Digital privacy heroes',
        'License :: OSI Approved :: BSD License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
'''

def yes_or_no(strquestion, default=None, intljust=65):
    answer = ""
    while answer not in ('y','n','yes','no'):
        question = '%s' % strquestion
        if default == "y":
            strdefault = red("y")
        elif default == "n":
            strdefault = green("n")
        else:
            strdefault = str(default)
        answer = raw_input(question.ljust(intljust," ")  + '(y/n) [%s] :' % strdefault)
        if answer == "" and default != None:
            answer = default
    return answer[0]

def green(string):
    return '\033[01;32m%s\033[00m' % string
    
def red(string):
    return '\033[01;31m%s\033[00m' % string

def main():
    failures = False
    try:
        a = settings.DATABASES
    except:
        print 'You should setup the database variables first!'
        return False
    
    commands = [
                    'pip install -r requirements.txt',
                    'mkdir toolbox/logs',
                    './manage.py syncdb --noinput',
                    './manage.py migrate toolbox --noinput',
                    './manage.py collectstatic --noinput',
                    './manage.py loaddata setup_db_content.json'
               ]

    i = 0   
    for command in commands:
        i += 1
        cmdsplit = shlex.split(command)
        
        print "Running: %s" % command
        
        cmd = subprocess.Popen(cmdsplit, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        for line in iter(cmd.stdout.readline, b''):
            print("> " + line.rstrip())
        
        # check exit code, if not 0 cancel the process..
        if cmd.poll() != 0:
            print '===\n\033[01;31mERROR this task failed.\n\033[00m==='
            failures = True
            if yes_or_no("This may not be a fatal error, do you want to continue?", default="n") == "n":
                break
        else: 
            print '===\n\033[01;32mTask %d out of %d completed succesfully.\n\033[00m===' % (i, len(commands))

    if failures:
        print '\033[01;31mSome task has failed, please see the readme for instructions!\n\033[00m==='
    else: 
        print '\033[01;32mCompleted all tasks.\n\033[00m'
        print '\033[01;43m\033[01;31mPlease run: `python manage.py createsuperuser` to create an administrator account for Django.\n\033[00m==='

if __name__ == "__main__":
   main()

# After this you can start the server (for testing ONLY!):
# python manage.py runserver 0.0.0.0:80 --insecure
