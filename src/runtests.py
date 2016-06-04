#!/usr/bin/env python2.7

import argparse
import os
import re
from subprocess import call, Popen, PIPE
import tempfile
import shutil

import logging

import git

def silent_do(args):
    with open(os.devnull, 'wb') as FNULL:
        return not call(args, stdout=FNULL, stderr=FNULL)

def stdout(args):
    with open(os.devnull, 'wb') as FNULL:
        p = Popen(args, stdout=PIPE, stderr=FNULL)
        stdout, stderr = p.communicate()
    return stdout


class TestRunner:

    def __init__(self, testdir, verbose=False, repo=None, cache=None):
        self.testdir = testdir
        self.cache = cache
        self.baserepo = repo or git.Repository(os.getcwd()) 

    def get_workdir(self, implv, testv):
        if self.cache:
            if not os.path.isdir(self.cache):
                os.mkdir(self.cache)
            return os.path.join(self.cache, "i{}-t{}".format(implv, testv))
        else:
            return tempfile.mkdtemp()

    def setup(self, implv, testv):
        workdir = self.get_workdir(implv, testv)
        if os.path.isdir(workdir) and git.Repository(workdir).is_repo():
            return git.Repository(workdir)
        else:
            logging.info("Creating new repo in %s", workdir)

            repo = self.baserepo.clone(workdir)
            repo.reset(implv, hard=True)

            with repo.in_context():
                logging.info("Fixing developer dependencies")
                repo.checkout(testv, files=["package.json"])
                deps = self.get_developer_dependencies()
                
                repo.checkout(implv, files=["package.json"])
                self.fix_developer_dependencies(deps)
                logging.info("Fixing developer dependencies [Done]")
                
                logging.debug("Installing npm dependencies")
                silent_do(["npm", "install"])
                logging.info("Installing npm dependencies [Done]")

                repo.checkout(testv, files=[self.testdir])
            return repo

    def get_developer_dependencies(self):
        p = Popen(["json", "-f", "package.json", "devDependencies"], stdout=PIPE, stderr=PIPE)
        out, _ = p.communicate()
        devDeps = "".join(out.strip().split("\n"))
        devDeps = devDeps.replace('"', '\"')
        return devDeps

    def fix_developer_dependencies(self, deps):
        silent_do(["json", "-I", "-f", "package.json", "-e", "this.devDependencies="+deps])
        should = stdout(["json", "-f", "package.json", "devDependencies.should"]).strip()
        if should == "*":
            silent_do(["json", "-I", "-f", "package.json", "-e",
                "this.devDependencies.should='<2'"])

    def check_deps(self):
        exists = silent_do(["which", "json"])
        if not exists:
            print "'json' tool is required. Try `npm install -g json`."
            exit(1)
    
    def run(self, implv, testv, testsuite):
        self.check_deps();
        logging.debug("Testing implv: %s, testv: %s, on suite \"%s\"", 
                implv, testv, testsuite)
        
        repo = self.setup(implv, testv) 

        with repo.in_context():
            logging.debug("In %s", os.getcwd())
            # Run tests (assume make test-jsapi at the moment)
            logging.info("Running tests")
            p = Popen(
                ["make", "-k", "test-" + testsuite], 
                stdout=PIPE, 
                stderr=PIPE, 
                universal_newlines=True
            )
            o, e = p.communicate()
            logging.debug(o)
            logging.debug("error:")
            logging.debug(e)
            logging.info("Running tests [Done]")

            # Parse stderr for errors
            errpat = "\d*\) (?P<err>.*):\s*$"
            violations = re.findall(errpat, o, re.MULTILINE) + re.findall(errpat, e, re.MULTILINE)

            unique_violations = sorted(set(violations))
                
            for viol in unique_violations:
                logging.info("Found violations: %s", viol)

            return [(implv, testv, violation) for violation in unique_violations]

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--impl", "-i", required=True,
                   help="Implementation version")
    p.add_argument("--test", "-t", required=True,
                   help="Test version")
    p.add_argument("--test-dir", "-d", required=True,
                   help="The test directory name")
    p.add_argument("--repo-dir", "-r",
                   help="The directory containing the repository")
    p.add_argument("--cache", "-c",
                   help="A cache folder, which can contain diferent versions of the file")
    p.add_argument("--verbose", "-v", action="count",
                   help="Print verbose output")
    p.add_argument("--test-suite", "-s", choices=["all", "unit", "jsapi"],
                   required=True,
                   help="Test suite to run")

    args = p.parse_args()

    if args.verbose == 1:
        logging.basicConfig(level=logging.INFO)
    if args.verbose == 2:
        logging.basicConfig(level=logging.DEBUG)

    repo = git.Repository(args.repo_dir or os.getcwd())
    tr = TestRunner(args.test_dir, repo=repo, cache=args.cache) 
    deps = tr.run(args.impl, args.test, args.test_suite)

    for dep in deps:
        print ",".join(dep)


if __name__ == "__main__":
    main()
        
