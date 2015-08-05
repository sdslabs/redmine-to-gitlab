#!/usr/bin/env python2

import conf
import requests
import base

con = base.Controller()

def get( url, load = {}):
    load['private_token'] = conf.token
    r = requests.get(conf.base_url + url, params = load, verify = conf.sslverify)
    if r.status_code != 200:
        return False
    return r.json()

def put( url, load = {}):
    load['private_token'] = conf.token
    r = requests.put(conf.base_url + url, params = load, verify = conf.sslverify)
    return r.json()


def post( url, load = {}):
    load['private_token'] = conf.token
    r = requests.post(conf.base_url + url, params = load, verify = conf.sslverify)
    return r.json()

def delete( url, load = {}):
    load['private_token'] = conf.token
    r = requests.delete(conf.base_url + url, params = load, verify = conf.sslverify)
    return r.json()

def redget( url, load = {}):
    load['key'] = conf.redmine_token
    r = requests.get(conf.redmine_base + url, params = load, verify = conf.sslverify)
    print r
    if r.status_code != 200:
        return False
    return r.json()

def redpost( url, load = {}):
    load['key'] = conf.redmine_token
    r = requests.post(conf.redmine_base + url, params = load, verify = conf.sslverify)
    return r.json()


#projects = get('/projects/all', {'page':1, 'per_page':500})
#projects.extend(get('/projects/all', {'page':2, 'per_page':500}))
projects = [{'id':1, 'name':'ep'}]

#redmine_projects = redget('/projects.json', {'limit':100, 'offset':0})['projects']
#redmine_projects.extend(redget('/projects.json', {'limit':100, 'offset':100})['projects'])

#print len(redmine_projects)

rawtimeentries = redget('/time_entries.json', {'limit':1000})
timeentries = {}
for rte in rawtimeentries['time_entries']:
    print str(rte['issue']['id']) + '-> ' + str(rte['hours'])

exit

def find_redmine_id(name):
    if (name == 'ep'):
            return 1

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
        issues.extend(redget('/issues.json', {'project_id': pid, 'limit':100, 'offset': 100*(i + 1), 'status_id':'*', 'include':'journals'})['issues'])

    print len(issues)

    for i in issues:
        if (i['id'] >= 807):
            details = redget('/issues/' + str(i['id']) + '.json', {'include':'journals'})['issue']
            if ('journals' in details):
                for journal in details['journals']:
                    if ('notes' in journal):
                        print journal['notes']
                    else:
                        print 'no notes'
            else:
                print 'no journals'
            #for k, v in details.iteritems():
            #    print k + ' -> ' + repr(v)

    #continue
    for issue in reversed(issues):
        print str(issue['id'])
        gitissue = get('/projects/' + str( pro['id']) + '/issues/' + str(issue['id']))
        if (not gitissue):
            newissue = {}
            newissue['id'] = pro['id']
            newissue['title'] = issue['subject']
            gitissue = post('/projects/' + str(pro['id']) + '/issues', newissue)
        else:
            print gitissue

        gitissue['description'] = issue["description"]
        #if 'assigned_to' in issue:
            #auser = con.finduserbyname(issue['assigned_to']['name'])
            #if(auser):

        gitissue['assignee_id'] = 2
        if ('fixed_version' in issue):
            gitissue['milestone_id'] = issue['fixed_version']['id']
        put('/projects/' +str(pro['id']) + '/issues/' + str(gitissue['id']), gitissue)

        details = redget('/issues/' + str(issue['id']) + '.json', {'include':'journals'})['issue']
        if ('journals' in details):
            for journal in details['journals']:
                if ('notes' in journal):
                    if (journal['notes']):
                        post('/projects/'+str(pro['id'])+ '/issues/' + str(gitissue['id']) + '/notes', {'id':pro['id'], 'issue_id':gitissue['id'],'body':journal['notes']})
                else:
                    print 'no notes'
        else:
            print 'no journals'

        #continue
        if (issue['status']['id'] == 5):
            put('/projects/' +str(pro['id'])+ '/issues/' + str(gitissue['id']), {'id':pro['id'], 'issue_id':gitissue['id'], 'state_event':'close'})
