#! /usr/local/bin/python
import time
from subprocess import Popen

print "\n*** starting metadata server at localhost:4000 ***\n"
md_p = Popen("python manage.py runserver --port=4000",  # > /dev/null 2>&1",
             shell=True)

print "\n*** starting front end server at localhost:8000 ***\n\n"
md_p = Popen("cd frontend && python -m SimpleHTTPServer",  # > /dev/null 2>&1",
             shell=True)

print "---------------------------------------------------------------------"
print "Both servers have successfully started. Visit http://localhost:8000"
print "to see the front end and to see some sample xml of default_form.json "
print "that the server emits, visit http://localhost:4000/api/metadata/" +\
    str(id) + "/xml.  Remove '/xml' to see the original json."
print "----------------------------------------------------------------------"

while True:
    time.sleep(1)
