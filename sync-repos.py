#!/usr/bin/env python3

import sys
from os import chdir, system, path, makedirs, listdir
import subprocess

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
    print("    changing dir to " + basepath)
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

def ci(repo: Repo):
    if not path.exists("ci-state"):
        print("    creating ci-state directory")
        makedirs("ci-state")


    filename = "ci-state/" + repo.reponame

    print("    reading " + filename)

    # get last known hash
    hash = ""
    if path.exists(filename):
        with open(filename, "r") as file:
            hash = str(file.read()).strip()

    # get current hash of repo
    chdir(r.dirname)

    command = "git log | grep commit | head -1"
    content = subprocess.check_output(["sh", "-c", command], shell=True, universal_newlines=True)
    newhash = content.replace("commit", "").strip()

    # if the hash hasn't changed, no new commits were added.
    # nothing left to do!
    if hash == newhash:
        chdir("..")
        return


    print("    performing ci for " + repo.reponame)
    print("    new hash is " + newhash)

    # else, update the hash
    with open("../" + filename, "w") as file:
        file.write(newhash)

    # and perform ci

    if path.exists("ci"):
        scripts = listdir("ci")
        scripts.sort()
        for script in scripts:
            print(f"\n\n    executing {script}")
            fullname = "ci/" + script
            system(fullname)


    chdir("..")







repos = list(parseRepos(content))

for r in repos:
    print("    syncing " + r.dirname)
    # if repo exist, update repo
    # otherwise fetch it from github
    if path.exists(r.dirname):
        chdir(r.dirname)
        system("git pull")
        chdir("..")
    else:
        system(f"git clone http://github.com/nilsmartel/{r.reponame} {r.dirname}")

    ci(r)
