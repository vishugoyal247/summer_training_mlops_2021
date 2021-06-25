#!/usr/bin/python3


print("content-type: text/html")
print()
import cgi
import subprocess



form = cgi.FieldStorage()
cmd = form.getvalue("x")
a = subprocess.getoutput("sudo\t"  +  cmd)
print(a)

