#!/env python3

import sys
from os import chdir, system, path

def inputfile():
    if len(sys.argv) == 2:
        return sys.argv[1]
    return "sync-repos"

class Repo:
    def __init__(self, dirname, reponame):
        self.dirname = dirname
        self.reponame = reponame

repofile = inputfile()

# change into directory of file
if "/" in repofile:
    [basepath, newrepo] = repofile.rsplit("/", maxsplit=1)
    chdir(basepath)
    repofile = newrepo

content = ""
with open(repofile, "r") as file:
    content = str(file.read())

def parseRepos(repocontent):
    for line in repocontent.splitlines():
        line = line.strip()
        if line == "":
            continue

        info = line.split(" ", maxsplit=1)
        if len(info) == 1:
            info.append(info[0])

        reponame, dirname = info

        yield Repo(dirname, reponame)

repos = list(parseRepos(content))

for r in repos:
    print("    fetching " + r.dirname)
    # if repo exist, update repo
    # otherwise fetch it from github
    if path.exists(r.dirname):
        os.chdir(r.dirname)
        system("git pull")
        os.chdir("..")
    else:
        system(f"git clone https://github.com/nilsmartel/{r.reponame} {r.dirname}")
