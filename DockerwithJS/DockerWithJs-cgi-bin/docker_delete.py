#!/usr/bin/python3

print("content-type: text/html")
print()

import subprocess as sp
import cgi

form = cgi.FieldStorage()
cmd = form.getvalue("imagename")
a=sp.getoutput("sudo docker rm -f {}".format(cmd))
print(a)

