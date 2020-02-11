import sys
import os


out = os.popen("git pull origin master")
print(out.read())
out = os.popen("flake8")
test = out.read()
if len(str(test)):
    print(test)
    exit()
print("No Flake8 Errors")
out = os.popen("git add .")
print(out.read())
out = os.popen("git commit -m " + "\"" + " ".join(sys.argv[1:]) + "\"")
print(out.read())
out = os.popen("git push origin master")
print(out.read())
