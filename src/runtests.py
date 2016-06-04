#!/usr/bin/env python2.7

import argparse
import os
import re
from subprocess import call, Popen, PIPE
import tempfile
import shutil

import git

class TestRunner:

    def __init__(self, testdir, verbose=False, repodir=None):
        self.testdir = testdir
        self.verbose = verbose
        if not repodir:
            self.repodir = os.getcwd()
        else:
            self.repodir = repodir

    def __enter__(self):
        self.wdir = tempfile.mkdtemp()
        return self
    
    def __exit__(self, type, value, traceback):
        os.chdir(self.repodir)
        shutil.rmtree(self.wdir)

    def run(self, implv, testv, testsuite):
        if self.verbose:
            print "Testing implv: " + implv + ", testv: " + testv + \
                ", on suite \"" + testsuite + "\""
            
        with open(os.devnull, 'w') as FNULL:
            # Clone into work dir
            git.clone(self.repodir, self.wdir)

            os.chdir(self.wdir)
        
            # Reset to implv
            git.reset_hard(implv)

            # Check for the "json" tool
            ret = call(["which", "json"], stdout=FNULL, stderr=FNULL)
            if ret:
                print "'json' tool is required. Try `npm install -g json`."
                exit(1)
                
            # Get devDeps from test package.json
            git.co_by_tag(testv, "package.json")
            
            p = Popen(["json", "-f", "package.json", "devDependencies"], stdout=PIPE, stderr=PIPE)
            devDeps, _ = p.communicate()
            devDeps = "".join(devDeps.strip().split("\n"))
            devDeps = devDeps.replace('"', '\"')
            
            # Put test devDeps into impl devDeps
            git.co_by_tag(implv, "package.json")

            call(["json", "-I", "-f", "package.json", "-e", "this.devDependencies="+devDeps],
                 stdout=FNULL, stderr=FNULL)

            p = Popen(["json", "-f", "package.json", "devDependencies.should"], stdout=PIPE, stderr=PIPE)
            should = p.communicate()[0].strip()

            if should == "*":
                call(["json", "-I", "-f", "package.json", "-e", "this.devDependencies.should='<2'"],
                     stdout=FNULL, stderr=FNULL)

            # npm install
            call(["npm", "install"], stdout=FNULL, stderr=FNULL)

            # checkout test dir from testv
            git.co_by_tag(testv, self.testdir)

            # Run tests (assume make test-jsapi at the moment)
            p = Popen(["make", "-k", "test-" + testsuite], stdout=PIPE, stderr=PIPE, universal_newlines=True)
            o, e = p.communicate()

            # Parse stderr for errors
            errpat = "\d*\) (?P<err>.*):\s*$"
            m = re.findall(errpat, o, re.MULTILINE) + re.findall(errpat, e, re.MULTILINE)

            m = list(set(m))

            if m and self.verbose:
                for viol in m:
                    print "Found violation: " + viol

            return [(implv, testv, v) for v in m]

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
    p.add_argument("--verbose", "-v", action="store_true",
                   help="Print verbose output")
    p.add_argument("--test-suite", "-s", choices=["all", "unit", "jsapi"],
                   required=True,
                   help="Test suite to run")

    args = p.parse_args()

    if args.repo_dir:
        repodir = os.path.abspath(args.repo_dir)
    else:
        repodir = os.getcwd()
        
    with TestRunner(args.test_dir, repodir=repodir, verbose=args.verbose) as tr:
        tr.run(args.impl, args.test, args.test_suite)


if __name__ == "__main__":
    main()
        
