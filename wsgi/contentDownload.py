#! /usr/bin/env python
# -*- coding: utf-8 -*-
import owncloud
import os

# Takes as input a list of remote filepaths and put them on the local machine

# Parameters
# Root directory of content on machine
data_root_dir = "/home/pi/data"
username = ""
password = ""

# Connecting to the NextCloud Server
c = owncloud.Client('http://54.224.18.48/nextcloud/')
c.login(username, password)

# Given a remote path, returns the local path to save a file, generating
# all necessary directories
def get_local_path(path):
  split_path = path.split("/")
  # Dirs that need to exist in local (removing filename at end and root dirs at beg)
  path_dirs = split_path[2:-1]
  data_dir = data_root_dir
  # Making all nec dirs
  for dir in path_dirs:
    data_dir = data_dir + "/" + dir
    if not os.path.exists(data_dir):
      os.makedirs(data_dir)
  data_dir = data_dir + "/" + split_path[-1]
  return data_dir

remote_paths = []
remote_paths.append("/BibleBox/audio/English_English_Standard_Version____NT_Drama/B27___1$

# Save each item in the list of files into the local directory in the same structure
for path in remote_paths:
  local_path = get_local_path(path)
  c.get_file(path, local_path)
print "Done"