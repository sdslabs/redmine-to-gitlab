#!/usr/bin/env python2

import requests
import urllib
import conf
import base

redmine_base = 'https://redmine.yourdomain.com'
redmine_token = ''

con = base.Controller()

def get( url, load = {}):
    load['private_token'] = conf.token
    r = requests.get(conf.base_url + url, params = load)
    return r.json()

def put( url, load = {}):
    load['private_token'] = conf.token
    r = requests.put(conf.base_url + url, params = load)
    return r.json()


def post( url, load = {}):
    load['private_token'] = conf.token
    r = requests.post(conf.base_url + url, params = load)
    return r.json()


def redget( url, load = {}):
    load['key'] = redmine_token
    r = requests.get(redmine_base + url, params = load)
    print r
    if r.status_code != 200:
        return False
    return r.json()

def find_gitlab_repo(name):
    for pro in projects:
        if ( pro['name'].lower() == name.lower()):
            return pro
    return False


def find_redmine_name(name):
    for pro in redmine_projects:
        if ( pro['identifier'].lower() == name.lower()):
            return pro['identifier']

    return false



projects = get('/projects/all', {'page':1, 'per_page':500})
projects.extend(get('/projects/all', {'page':2, 'per_page':500}))

redmine_projects = redget('/projects.json', {'limit':100, 'offset':0})['projects']
redmine_projects.extend(redget('/projects.json', {'limit':100, 'offset':100})['projects'])
for repo in redmine_projects:
    gitlab = find_gitlab_repo(repo['identifier'])
    if ( not gitlab ):
        print repo['identifier']
	#Here namespace_id is the id of the group/user namespace to which the projects are to be imported
        print post('/projects', {'name': repo['identifier'], 'namespace_id': 4})
