#! /usr/bin/env python
import owncloud
import json

mimes = {
	'application/vnd.android.package-archive': 'software'
}

def ownCloudList(client_url, username, password, root):
	json_data = {}
	files = {}

	c = owncloud.Client(client_url)
	c.login(username, password)

	for file_info in c.list(root, depth='infinity'):
		if not file_info.is_dir():
			mimetype = file_info.get_content_type()
			file_type = mimetype.split('/')[0]
			if file_type not in ['audio', 'video', 'image']:
				file_type = mimes.get(mimetype)
				if file_type is None:
					file_type = 'text'

			f = files.setdefault(file_type, [])
			f.append((file_info.name, file_info.path, mimetype))
			
	json_data['root'] = [files]

	#with open('filenames.json', 'w') as json_file:
	print json.dumps(json_data, sort_keys=True,
	                  indent=4, separators=(',', ': '))


if __name__ == '__main__':
	import sys
	ownCloudList(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])