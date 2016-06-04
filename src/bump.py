#!/usr/bin/env python

import argparse
import os
import shutil
from subprocess import call, Popen, PIPE
import tempfile
import re
import sys
import logging

import git
import semver
import runtests

def dv(runner, suite, history, v):
    in_minor_v = semver.get_prev_in_minor(history, v)
    in_major_v = semver.get_prev_in_major(history, v)
        
    for patch_v in in_minor_v:
        for violation in runner.run(patch_v, v, suite):
            yield violation
   
    for minor_v in in_major_v:
        for violation in runner.run(v, minor_v, suite):
            yield violation


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--test-dir", "-d", required=True,
                   help="The folder in which the api tests reside.")
    p.add_argument("test_version",
                   help="A version to test bumping to.")
    p.add_argument("--repository", "-r",
                   help="Path to repository on the system, default is CWD")
    p.add_argument("--cache", "-c",
                   help="A cache of results")
    # p.add_argument("--test-script", "-t",
    #                help="Shell script to run tests.")
    p.add_argument("--verbose", "-v", action="count",
                   help="Run with verbose output.")
    # p.add_argument("--report-violations", action="store_true",
    #                help="Report violation information")
    p.add_argument("--test-suite", "-s", choices=["all", "unit", "jsapi"],
                   required=True,
                   help="The test suite to run")
    
    args = p.parse_args()
    
    if args.verbose == 1:
        logging.basicConfig(level=logging.INFO)
    if args.verbose == 2:
        logging.basicConfig(level=logging.DEBUG)

    repo = git.Repository(args.repository)

    if not repo.is_repo():
        error("Not currently in a git repository")

    branch = repo.current_branch() 
    if branch != "master":
        error("Must be on the master branch, was on " + branch)
    
    tags = semver.sort(repo.get_tags())

    if not semver.valid(args.test_version):
        error(args.test_version + ' is not valid SemVer')
    
    if args.test_version not in tags:
        error('Version ' + args.test_version + ' not in history')
    
    runner = runtests.TestRunner(
        args.test_dir, 
        repo=repo, 
        cache=os.path.abspath(args.cache)
    )
    for violation in dv(runner, args.test_suite, tags, args.test_version):
        print "V{},{},{},{!r}".format(args.test_version, *violation)

def error(msg=None):
    if msg:
        print 'Error: ' + msg
    exit(1)

if __name__ == "__main__":
    main()
