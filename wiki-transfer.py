#!/usr/bin/env python2

import requests
import urllib
import conf
import base

redmine_base = 'https://redmine.yourdomain.co.in'
redmine_token = ''

gitlab_cookie = ''
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

def find_redmine_name(name):
    for pro in redmine_projects:
        if ( pro['identifier'].lower() == name.lower()):
            return pro['identifier']

    return False



def getauthtoken(project, wikiname):
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' , 'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate, sdch', 'Cookie': 'request_method=GET; _gitlab_session=' + gitlab_cookie  , 'Accept-Language': 'en-US,en;q=0.8', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36'}
    r = requests.get( 'https://gitlab.sdslabs.co.in/sdslabs/' + project + '/wikis/' + wikiname, headers = headers)
    rsp = r.text
    return rsp.partition('" name="csrf-token" />')[0][-44:]

def createdata(token, title, body, message):
    f = {'authenticity_token': token, 'wiki[title]': title, 'wiki[format]': 'markdown', 'wiki[content]': body, 'wiki[message]' : message, 'utf-8':u'\xe2\x9c\x93'}
    return f


projects = get('/projects/all', {'page':1, 'per_page':500})
projects.extend(get('/projects/all', {'page':2, 'per_page':500}))

redmine_projects = redget('/projects.json', {'limit':100, 'offset':0})['projects']
redmine_projects.extend(redget('/projects.json', {'limit':100, 'offset':100})['projects'])


def createwiki(project, title, body):
    headers = {'Origin': 'https://gitlab.sdslabs.co.in' , 'Referer': 'https://gitlab.sdslabs.co.in/sdslabs/' + project + '/wikis/' + title,'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' , 'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate', 'Cookie': '_gitlab_session=' + gitlab_cookie  ,'Content-Type': 'application/x-www-form-urlencoded' , 'Accept-Language': 'en-US,en;q=0.8', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36'}
    r = requests.post('https://gitlab.sdslabs.co.in/sdslabs/'+ project + '/wikis', headers = headers, data = body)
    print r.status_code
    return r.text

def deletewiki(project, title, token):
    body = {'_method':'delete','authenticity_token':token}
    headers = {'Pragma': 'no-cache','Origin': 'https://gitlab.sdslabs.co.in', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-US,en;q=0.8', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36', 'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Cache-Control': 'no-cache', 'Referer':
    'https://gitlab.sdslabs.co.in/sdslabs/' + project + '/wikis/' + title + '/edit', 'Cookie': 'default_view=%23tab-activity; sds_login=a6501875a8be8a49b04afc28da2743b0; default_view=%23tab-activity; request_method=GET; _gitlab_session=' + gitlab_cookie, 'Connection': 'keep-alive' }
    r = requests.post('https://gitlab.sdslabs.co.in/sdslabs/'+ project + '/wikis/' + title, headers = headers, data = body)
    print r.status_code
    return r


for pro in projects:
    print pro['name']
    pname= find_redmine_name(pro['name'])

    if(not pname):
        continue

    rsp = redget('/projects/' + pname + '/wiki/index.json')
    if (not rsp):
        continue
    no_of_wikis = len(rsp['wiki_pages'])
    wikies_list = rsp['wiki_pages']


    print len(wikies_list)

    for wiki in reversed(wikies_list):
        wiki_details = redget('/projects/' + pname + '/wiki/' + wiki['title'] + '.json')['wiki_page']
        print wiki_details
        if ( wiki_details['title'].lower() == 'wiki'):
            wiki_details['title'] = 'home'

        newwiki= {}
        newwiki['project'] = pro['name']
        newwiki['title'] = wiki_details['title']
        newwiki['body'] = wiki_details['text']
        newwiki['message'] = wiki_details['comments']
        newwiki['name'] = wiki_details['title'].lower()
        if 'author' in wiki_details:
            auser = con.finduserbyname(wiki_details['author']['name'])
            if(auser):
                newwiki['sudo'] = auser['id']

        print newwiki
        token = getauthtoken(newwiki['project'], newwiki['title'])
        data = createdata(token, newwiki['title'], newwiki['body'], newwiki['message'])
        rsp = createwiki(newwiki['project'], newwiki['title'], data)
