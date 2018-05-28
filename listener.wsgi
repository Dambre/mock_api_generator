#!/usr/bin/python3

activate_this = '/home/ubuntu/projects/CMFPythonMockServer/env/bin/activate_this.py'
exec(open(activate_this).read(), dict(__file__=activate_this))

import sys

sys.path.insert(0, '/home/ubuntu/projects/CMFPythonMockServer')

from listener import app as application
