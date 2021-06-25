#!/usr/bin/python3

print("content-type: text/html")
print()

import subprocess as sp
a=sp.getoutput("sudo docker ps -a")
print(a)


