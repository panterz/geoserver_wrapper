from fabric.api import env, hosts, lcd, local, task, run, put, prompt, sudo
import os
import getpass

CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))

@task
def deploy_local():
    """Defines local environment"""
    env.local = 'local'
    env.app_name = "geoserver_wrapper"
    env.base_dir = os.sep.join((os.environ['HOME'], env.local))
    env.domain_path = "%(base_dir)s/%(app_name)s" % {'base_dir': env.base_dir, 'app_name': env.app_name}
    env.env_file = os.sep.join((CURRENT_PATH, "etc", "requirements.txt"))

    if os.path.exists(env.domain_path):
        # check if they want to delete existing installation
        msg = 'Directory %s exists.\nDo you wish to delete it(y/n)? > '
        msg = msg % env.domain_path
        answer = raw_input(msg).strip()

        if answer != 'y':
            print 'Choosing not continue. Nothing installed.'
            return

        local('rm -rf {0}'.format(env.domain_path))

    with lcd(env.base_dir):
        local('virtualenv {0}'.format(env.app_name))

    with lcd(env.domain_path):
        # initialise virtual environment
        _virtualenv('pip -q install -r {0}'.format(env.env_file))

        local("ln -s %(current_path)s/src %(domain_path)s/src" % { 'current_path': CURRENT_PATH, 'domain_path':env.domain_path})
        local("mkdir {0}/data".format(env.domain_path))
        local("sudo chown {0}:www-data {1}/data".format(getpass.getuser(), env.domain_path))
        local("chmod 775 {0}/data/".format(env.domain_path))
        local("mkdir {0}/logs".format(env.domain_path))
        local("sudo chown {0}:www-data {1}/logs/".format(getpass.getuser(), env.domain_path))
        local("chmod 775 {0}/logs/".format(env.domain_path))



def _virtualenv(command):
    """run command using virtual environment and the current runtime directory"""
    local('. %s/bin/activate && %s' % (env.domain_path, command))
