#! /usr/bin/env python

import json
import os
import os.path
import sys

import webapp2
if os.path.dirname(__file__) not in sys.path:
    sys.path.append(os.path.dirname(__file__))

import owncloud


mimes = {
    'application/vnd.android.package-archive': 'software'
}

categories = [
    'audio',
    'images',
    'software',
    'text',
    'video'
]

data_root_dir = "/var/www/biblebox/biblebox_default"


class GetFileList(webapp2.RequestHandler):
    
    def post(self):
        
        try:
            client_url = self.request.get('client_url')
            username = self.request.get('username')
            password = self.request.get('password')
            folder_root = self.request.get('folder_root')
            if folder_root is None:
                raise ValueError("Must specify folder root")
            
            json_data = {}
            files = {}
        
            c = owncloud.Client(client_url)
            c.login(username, password)
        
            for file_info in c.list(folder_root, depth='infinity'):
                if not file_info.is_dir():
                    mimetype = file_info.get_content_type()
                    file_type = mimetype.split('/')[0]
                    if file_type == 'image':
                        file_type = 'images'
                        
                    if file_type not in ['audio', 'video', 'image']:
                        file_type = mimes.get(mimetype)
                        if file_type is None:
                            file_type = 'text'
        
                    f = files.setdefault(file_type, [])
                    f.append((file_info.name, file_info.path, mimetype))
                    
            json_data['root'] = [(k, v) for k, v in files.iteritems()]
            json_data['status'] = 'OK'
        
            #with open('filenames.json', 'w') as json_file:
            content = json.dumps(json_data, sort_keys=True,
                              indent=4, separators=(',', ': '))
        except Exception as e:
            content = json.dumps({'status': 'ERROR', 'error': str(e)})
        
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(content)


class GetContent(webapp2.RequestHandler):
    
    def post(self):
        
        client_url = self.request.get('client_url')
        username = self.request.get('username')
        password = self.request.get('password')
        paths = self.request.get('paths')
        
        # list of [remote_path, category, filename]
        paths = json.loads(paths)['root']

        # Connecting to the NextCloud Server
        c = owncloud.Client(client_url)
        c.login(username, password)
        
        # Save each item in the list of files into the local directory in the same structure
        for remote_path, category, filename in paths:
            if category in categories:
                local_path = os.path.join(data_root_dir, category, os.path.basename(filename))
                local_dir = os.path.dirname(local_path)
                if not os.path.exists(local_dir):
                    os.makedirs(local_dir)
                c.get_file(remote_path, local_path)
        
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps({'status': 'OK'}))

handlers = [
    ('/app/getfilelist/', GetFileList),
    ('/app/getcontent/', GetContent)
]

config = {}
debug = False

# Debug use only
static = os.environ.get('DEBUG')
if static:
    
    import mimetypes
    
    static_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
    
    class StaticFileHandler(webapp2.RequestHandler):
        def get(self, path):
            abs_path = os.path.abspath(os.path.join(static_root, path))
            if os.path.isdir(abs_path) or abs_path.find(static_root) != 0:
                self.response.set_status(403)
                return
            try:
                with open(abs_path, 'r') as fp:
                    self.response.headers.add_header('Content-Type', mimetypes.guess_type(abs_path)[0])
                    self.response.out.write(fp.read())
            except:
                self.response.set_status(404)
    
    debug = True
    handlers.append((r'/static/(.+)', StaticFileHandler))

application = webapp2.WSGIApplication(handlers, debug=debug, config=config)
    
