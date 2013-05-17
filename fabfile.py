# ~/fabfile.py
# A Fabric file for carrying out various administrative tasks with InaSAFE.
# Tim Sutton, Jan 2013

import os
from fabric.api import *
from datetime import datetime
from fabric.contrib.files import contains, exists, append, sed
import fabtools
from fabtools import require
from fabgis import fabgis
# Don't remove even though its unused
from fabtools.vagrant import vagrant

# Usage for localhost commands:
# fab localhost [command]
#  e.g. fab localhost update
# To run remotely do
#  fab remote [command]
# e.g.
# fab -H 188.40.123.80:8697 show_environment
# To run on a vagrant vhost do
# fab vagrant show_environment
#  e.g. fab vagrant show_environment
#
# Note: Vagrant tasks will only run if they @task decorator is used on
#       the function. See show_environment function below.

# Usage fab localhost [command]
#    or fab remote [command]
#  e.g. fab localhost initialise_qgis_plugin_repo

# Global options
env.env_set = False


def _all():
    """Things to do regardless of whether command is local or remote."""
    if env.env_set:
        fastprint('Environment already set!\n')
        return

    fastprint('Setting environment!\n')
    # Key is hostname as it resolves by running hostname directly on the server
    # value is desired web site url to publish the repo as.
    doc_site_names = {
        'cunonia': 'inasafe-docs.localhost',
        'waterfall': 'inasafe-docs.localhost',
        'spur': 'inasafe-docs.localhost',
        'maps.linfiniti.com': 'inasafe-docs.linfiniti.com',
        'linfiniti': 'inasafe-docs.linfiniti.com',
        #vagrant instance
        'precise64': 'inasafe-docs.vagrant.localhost',
        'shiva': 'docs.inasafe.org'}
    repo_site_names = {
        'cunonia': 'inasafe-docs.localhost',
        'waterfall': 'inasafe-docs.localhost',
        'spur': 'inasafe-docs.localhost',
        'maps.linfiniti.com': 'inasafe-docs.linfiniti.com',
        'linfiniti': 'inasafe-crisis.linfiniti.com',
        #vagrant instance
        'inasafe': 'experimental.vagrant.localhost',
        'shiva': 'experimental.inasafe.org'}

    with hide('output'):
        env.user = run('whoami')
        env.hostname = run('hostname')
        if env.hostname not in repo_site_names:
            print 'Error: %s not in: \n%s' % (env.hostname, repo_site_names)
            exit()
        elif env.hostname not in doc_site_names:
            print 'Error: %s not in: \n%s' % (env.hostname, repo_site_names)
            exit()
        else:
            env.repo_site_name = repo_site_names[env.hostname]
            env.doc_site_name = doc_site_names[env.hostname]
            env.inasafe_web_path = '/home/web/inasafe-docs'
            env.home = os.path.join('/home/', env.user)
            env.repo_path = os.path.join(env.home,
                                         'dev',
                                         'python')
            env.git_url = 'git://github.com/AIFDR/inasafe-doc.git'
            env.code_path = os.path.join(env.repo_path, env.repo_alias)

    env.env_set = True
    fastprint('env.env_set = %s' % env.env_set)

###############################################################################
# Next section contains helper methods tasks
###############################################################################


def update_git_checkout(branch='master'):
    """Make sure there is a read only git checkout.
    Args:
        branch: str - a string representing the name of the branch to build
            from. Defaults to 'master'
    To run e.g.::
        fab -H 188.40.123.80:8697 remote update_git_checkout
    """
    _all()
    fabtools.require.deb.package('git')
    if not exists(env.code_path):
        fastprint('Repo checkout does not exist, creating.')
        run('mkdir -p %s' % env.repo_path)
        with cd(env.repo_path):
            run('git clone %s %s' % (env.git_url, env.repo_alias))
    else:
        fastprint('Repo checkout does exist, updating.')
        with cd(env.code_path):
            # Get any updates first
            run('git fetch')
            # Get rid of any local changes
            run('git reset --hard')
            # Get back onto master branch
            run('git checkout master')
            # Remove any local changes in master
            run('git reset --hard')

    with cd(env.code_path):
        if branch != 'master':
            run('git branch --track %s origin/%s' %
                (branch, branch))
            run('git checkout %s' % branch)
        else:
            run('git checkout master')
        run('git pull')


@task
def build_doc(branch='master'):
    """Create a pdf and html doc tree and publish them online.
    Args:
        branch: str - a string representing the name of the branch to build
            from. Defaults to 'master'.
    To run e.g.::
        fab -H 188.40.123.80:8697 build_documentation
        or to package up a specific branch (in this case minimum_needs)
        fab -H 88.198.36.154:8697 build_documentation:version-1_1
    .. note:: Using the branch option will not work for branches older than 1.1
    """
    _all()
    update_git_checkout(branch)
    fabgis.fabgis.install_latex()

    dir_name = os.path.join(env.repo_path, env.repo_alias)
    with cd(dir_name):
        # build the Documentation
        run('chmod +x scripts/post_translate.sh')
        run('scripts/post_translate.sh')
        run('cp -r docs/output/html/* %s' % env.inasafe_web_path)
        run('cp -r docs/output/pdf %s' % env.inasafe_web_path)
        run('cp scripts/.htaccess %s' % env.inasafe_web_path)
        run('cp scripts/directory*.html %s/en/_static/' % env.inasafe_web_path)


@task
def initialise_docs_site():
    """Initialise an InaSAFE docs site where we host docs and pdf."""
    _all()
    build_doc()

    fabtools.require.deb.package('apache2')
    code_path = os.path.join(env.repo_path, env.repo_alias)
    local_path = '%s/scripts' % code_path

    if not exists(env.inasafe_web_path):
        sudo('mkdir -p %s' % env.inasafe_web_path)
        sudo('chown %s.%s %s' % (env.user, env.user, env.inasafe_web_path))

    run('cp %(local_path)s/inasafe-docs.conf.templ '
        '%(local_path)s/inasafe-docs.conf' % {'local_path': local_path})

    sed('%s/inasafe-test.conf' % local_path,
        'inasafe-docs.linfiniti.com',
        env.repo_site_name)

    with cd(code_path):
        # Copy built Documentation to the Webserver path
        run('cp -r docs/output/html/* %s' % env.inasafe_web_path)
        run('cp -r docs/output/pdf %s' % env.inasafe_web_path)
        run('cp scripts/.htaccess %s' % env.inasafe_web_path)
        run('cp scripts/directory*.html %s/en/_static/' % env.inasafe_web_path)

    with cd('/etc/apache2/sites-available/'):
        if exists('inasafe-docs.conf'):
            sudo('a2dissite inasafe-docs.conf')
            fastprint('Removing old apache2 conf', False)
            sudo('rm inasafe-docs.conf')

        sudo('ln -s %s/inasafe-docs.conf .' % local_path)

    # Add a hosts entry for local testing - only really useful for localhost
    hosts = '/etc/hosts'
    if not contains(hosts, 'inasafe-docs'):
        append(hosts, '127.0.0.1 %s' % env.repo_site_name, use_sudo=True)

    sudo('a2ensite inasafe-docs.conf')
    sudo('a2enmod rewrite')
    sudo('service apache2 reload')


@task
def show_environment():
    """For diagnostics - show any pertinent info about server."""
    _all()
    fastprint('\n-------------------------------------------------\n')
    fastprint('User: %s\n' % env.user)
    fastprint('Host: %s\n' % env.hostname)
    fastprint('Site Name: %s\n' % env.repo_site_name)
    fastprint('Dest Path: %s\n' % env.plugin_repo_path)
    fastprint('Home Path: %s\n' % env.home)
    fastprint('Repo Path: %s\n' % env.repo_path)
    fastprint('Git Url: %s\n' % env.git_url)
    fastprint('Repo Alias: %s\n' % env.repo_alias)
    fastprint('-------------------------------------------------\n')
