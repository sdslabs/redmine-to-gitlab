#!/usr/bin/env python2

import conf
import requests
import base
from subprocess import call

con = base.Controller()

#Your redmine authentication token
redmine_base = 'https://redmine.yourdomain.com'
redmine_token = ''

gitlab_cookie = ''

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

def getauthtoken():
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' , 'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate, sdch', 'Cookie': 'request_method=GET; _gitlab_session=' + gitlab_cookie  , 'Accept-Language': 'en-US,en;q=0.8', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36'}
    r = requests.get( conf.base_url[:-7] + '/admin/users/new', headers = headers)
    rsp = r.text
    return rsp.partition('" name="csrf-token" />')[0][-44:]


def getusers():

    rsp = redget('/users.json', {'limit':100})
    if (not rsp):
        return False
    no_of_users= rsp['total_count']
    users = rsp['users']
    for i in range(no_of_users//100):
        issues.extend(redget('/users.json', {'limit':100, 'offset': 100*(i + 1)})['users'])
    return users

def createuser(name, email, username):
    token = getauthtoken()
    request = "curl " + conf.base_url[:-7] + "'/admin/users' -H 'Pragma: no-cache' -H 'Origin: https://gitlab.sdslabs.co.in' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: en-US,en;q=0.8' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36' -H 'Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryxlXmrKoBhYyRspZw' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cache-Control: no-cache' -H 'Referer: https://gitlab.sdslabs.co.in/admin/users/new' -H 'Cookie: default_view=%23tab-activity; collapsed_nav=false; event_filter=team; _gitlab_session=" + gitlab_cookie + "; request_method=GET' -H 'Connection: keep-alive' --data-binary $'------WebKitFormBoundaryxlXmrKoBhYyRspZw\r\nContent-Disposition: form-data; name=\"utf8\"\r\n\r\n\u2713\r\n------WebKitFormBoundaryxlXmrKoBhYyRspZw\r\nContent-Disposition: form-data; name=\"authenticity_token\"\r\n\r\n" + token + "\r\n------WebKitFormBoundaryxlXmrKoBhYyRspZw\r\nContent-Disposition: form-data; name=\"user[name]\"\r\n\r\n" + name + "\r\n------WebKitFormBoundaryxlXmrKoBhYyRspZw\r\nContent-Disposition: form-data; name=\"user[username]\"\r\n\r\n" + username + "\r\n------WebKitFormBoundaryxlXmrKoBhYyRspZw\r\nContent-Disposition: form-data; name=\"user[email]\"\r\n\r\n" + email + "\r\n------WebKitFormBoundaryxlXmrKoBhYyRspZw\r\nContent-Disposition: form-data; name=\"user[projects_limit]\"\r\n\r\n0\r\n------WebKitFormBoundaryxlXmrKoBhYyRspZw\r\nContent-Disposition: form-data; name=\"user[can_create_group]\"\r\n\r\n0\r\n------WebKitFormBoundaryxlXmrKoBhYyRspZw\r\nContent-Disposition: form-data; name=\"user[admin]\"\r\n\r\n0\r\n------WebKitFormBoundaryxlXmrKoBhYyRspZw\r\nContent-Disposition: form-data; name=\"user[avatar]\"; filename=\"\"\r\nContent-Type: application/octet-stream\r\n\r\n\r\n------WebKitFormBoundaryxlXmrKoBhYyRspZw\r\nContent-Disposition: form-data; name=\"user[skype]\"\r\n\r\n\r\n------WebKitFormBoundaryxlXmrKoBhYyRspZw\r\nContent-Disposition: form-data; name=\"user[linkedin]\"\r\n\r\n\r\n------WebKitFormBoundaryxlXmrKoBhYyRspZw\r\nContent-Disposition: form-data; name=\"user[twitter]\"\r\n\r\n\r\n------WebKitFormBoundaryxlXmrKoBhYyRspZw\r\nContent-Disposition: form-data; name=\"user[website_url]\"\r\n\r\n\r\n------WebKitFormBoundaryxlXmrKoBhYyRspZw--\r\n' --compressed"
    print request
    print call ([request], shell = True)

users = getusers()

for user in users:
    name = user['firstname'].capitalize() + ' ' + user['lastname'].capitalize()
    email = user['mail']
    username = user['login']
    print name
    inp = input("Do you wawnt to add the user (Enter 1 for yes, anything else for no)")
    if (int(inp) == 1):
      createuser(name, email, username)

