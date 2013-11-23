# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import subprocess
from fabric.api import local, settings as fab_settings, lcd


def push(message, params=''):
    """ Push and deploy """
    local("git checkout master")
    local("git add --all .")
    local("git commit -m '%s'" % message)

    local("git checkout gh-pages")
    local("git rm -rf .")
    local('git read-tree -m -u master:output')
    local("git add --all .")
    local("git commit -m '%s'" % message)

    local("git checkout master")
    local("git push origin gh-pages %s" % params)
    local("git push origin master %s" % params)


def make():
    """ Generate the static files """
    local('pelican content -s pelican_settings.py')


def run():
    """ Generate and serve the static files """
    pelican = subprocess.Popen('pelican content -s pelican_settings.py --autoreload --verbose')
    httpd = subprocess.Popen('python -m SimpleHTTPServer', cwd='output')
    try:
        httpd.wait()
        pelican.wait()
    except:
        httpd.kill()
        pelican.kill()