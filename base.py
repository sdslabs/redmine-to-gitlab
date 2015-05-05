#!/usr/bin/python2
import conf
import requests

def get( url, load = {}):
    load['private_token'] = conf.token
    r = requests.get(conf.base_url + url, params = load)
    return r.json()

def post( url, load = {}):
    load['private_token'] = conf.token
    r = requests.post(conf.base_url + url, params = load)
    return r.json()

def delete( url, load = {}):
    load['private_token'] = conf.token
    r = requests.delete(conf.base_url + url, params = load)
    return r.json()




class Controller:
    """A class to run our custom commands"""

    def __init__(self, url = conf.base_url, token = conf.token):
        self.url = url
        self.token = token


    def getuser(self):
        if hasattr(self, 'user'):
            return self.user
        self.user = get('/user')

        return self.user



    def selfusername(self):
        if hasattr(self, 'user'):
            return self.user['username']

        return self.getuser()['username']

    def getuserlist(self):
        if hasattr(self, 'userlist'):
            return self.userlist

        self.userlist = get('/users', { 'per_page': 500, 'page':1})
        return self.userlist

    def finduserbyname(self, name):
        userlist = self.getuserlist()

        for user in userlist:
            if (user['name'].lower() == name.lower()):
                return user
        return False


    def finduser(self, username):
        userlist = self.getuserlist()

        for user in userlist:
            if (user['username'] == username):
                return user
        return False

    def addsshkey(self, username, sshkey):
        user = self.finduser(username)
        if (not user):
            return False

        res = post('/users/' + str(user['id']) + '/keys',{'id': user['id'], 'title': username, 'key': sshkey})
        return res

    def listsshkeys(self, username):
        user = self.finduser(username)
        if (not user):
            return False


        res = get('/users/' + str(user['id']) + '/keys',{'uid': user['id']})
        return res

    def deletekey(self, uid, keyid):
        res = delete('/users/' + str(uid) + '/keys/' + str(keyid), {'uid': uid, 'id':keyid})
        return res


    def deleteallkeys(self, username):
        keylist = self.listsshkeys(username)
        user = self.finduser(username)
        if (not user):
            return False


        for key in keylist:
            self.deletekey(user['id'], key['id'])

    def modifykeys(self, username, key):
        self.deleteallkeys(username)
        self.addsshkey(username, key)

    def adduser(self, email, password, username, name):
        res = post('/users', {'email':email, 'password':password, 'username': username, 'name':name})

        return res

    def removeuser(self, username):
        user = self.finduser(username)
        if (not user):
            return False

        res = delete('/users/' + str(user['id']), {'id':user['id']})

        return res

    def isadmin(self, username):
        user = self.finduser(username)
        if (not user):
            return False

        return user['is_admin']

    def getgroup(self, groupname):
        groupslist = get('/groups', {'search':groupname})
        for g in groupslist:
            if ( g['name'] == groupname):
                return g

        return False


    def isgroupmember(self, groupname, username):
        group = self.getgroup(groupname)
        if (not group):
            return False
        members = get('/groups/' + str(group['id']) + '/members', {'per_page':500})
        for user in members:
            if (user['username'] == username):
                return True
        return False







