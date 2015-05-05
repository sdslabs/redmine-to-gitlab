#!/usr/bin/env python2

import conf
import requests
import base

con = base.Controller()

#Your redmine authentication token
redmine_base = 'https://redmine.yourdomain.co.in'
redmine_token = ''

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

def delete( url, load = {}):
    load['private_token'] = conf.token
    r = requests.delete(conf.base_url + url, params = load)
    return r.json()

def redget( url, load = {}):
    load['key'] = redmine_token
    r = requests.get(redmine_base + url, params = load)
    print r
    if r.status_code != 200:
        return False
    return r.json()

def redpost( url, load = {}):
    load['key'] = redmine_token
    r = requests.post(redmine_base + url, params = load)
    return r.json()


projects = get('/projects/all', {'page':1, 'per_page':500})
projects.extend(get('/projects/all', {'page':2, 'per_page':500}))

redmine_projects = redget('/projects.json', {'limit':100, 'offset':0})['projects']
redmine_projects.extend(redget('/projects.json', {'limit':100, 'offset':100})['projects'])

print len(redmine_projects)


def find_redmine_id(name):
    for pro in redmine_projects:
        if ( pro['identifier'].lower() == name.lower()):
            return pro['id']

    return False

def getissues(name):
    pid = find_redmine_id(pro['name'])

    if(not pid):
        return False

    rsp = redget('/issues.json', {'project_id': pid, 'limit':100, 'status_id':'*'})
    if (not rsp):
        return False
    no_of_issues = rsp['total_count']
    issues = rsp['issues']
    for i in range(no_of_issues//100):
        issues.extend(redget('/issues.json', {'project_id': pid, 'limit':100, 'offset': 100*(i + 1), 'status_id':'*'})['issues'])
    return issues



for pro in projects:
    print pro['name']
    pid = find_redmine_id(pro['name'])

    if(not pid):
        continue

    rsp = redget('/issues.json', {'project_id': pid, 'limit':100, 'status_id':'*'})
    if (not rsp):
        continue
    no_of_issues = rsp['total_count']
    issues = rsp['issues']
    for i in range(no_of_issues//100):
        issues.extend(redget('/issues.json', {'project_id': pid, 'limit':100, 'offset': 100*(i + 1), 'status_id':'*'})['issues'])

    print len(issues)

    for issue in reversed(issues):
        newissue = {}
        newissue['id'] = pro['id']
        newissue['title'] = issue['subject']
        newissue['description'] = issue["description"]
        if 'assigned_to' in issue:
            auser = con.finduserbyname(issue['assigned_to']['name'])
            if(auser):
                newissue['assignee_id'] = auser['id']
        print newissue
        newiss = post('/projects/' + str(pro['id']) + '/issues', newissue)
        print newiss

        if (issue['status']['id'] == 5):
            put('/projects/' +str( pro['id']) + '/issues/' + str(newiss['id']), {'id':pro['id'], 'issue_id':newiss['id'], 'state_event':'close'})

