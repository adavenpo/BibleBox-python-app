#! /usr/bin/env python
import owncloud

c = owncloud.Client('http://54.224.18.48/nextcloud/')
c.login('admin', 'biblebox')
files = []
for i in c.list('/BibleBox'):
    files.append(str(i.path).split('/')[-2])

for i in files:
    print i
