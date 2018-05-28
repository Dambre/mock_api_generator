
from fabric.api import *
from fabric.context_managers import cd

env.user = 'ubuntu'
env.hosts = ['ec2-52-49-210-166.eu-west-1.compute.amazonaws.com']
env.activate = 'source env/bin/activate'


def deploy():
    with cd('~/projects/CMFPythonMockServer'):
        run('git pull origin master')
        with prefix(env.activate):
            run('pip install -r requirements.txt')
        run('sudo systemctl restart apache2.service')
    run('forever restartall')
