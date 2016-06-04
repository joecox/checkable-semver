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


def cvt(runner, history, v):
    in_minor_v = semver.get_prev_in_minor(history, v)
    in_major_v = semver.get_prev_in_major(history, v)
    
    for patch_v in in_minor_v:
        yield (runner, patch_v, v)
   
    for minor_v in in_major_v:
        yield (runner, v, minor_v)

def setup_test(t):
    runner, impl, test = t
    return runner.setup(impl, test).directory

def main():
    p = argparse.ArgumentParser()
    p.add_argument("version",
                   help="A version to test bumping to.")
    p.add_argument("--test-dir", "-d", required=True,
                   help="The folder in which the api tests reside.")
    p.add_argument("--repository", "-r",
                   help="Path to repository on the system, default is CWD")
    p.add_argument("--cache", "-c",
                   help="A cache of results")
    p.add_argument("--setup-only",
                action="store_true",
                help="if cache has been set, this method will run the setup only"
                )
    p.add_argument("--verbose", "-v", action="count",
                   help="Run with verbose output.")
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

    if not semver.valid(args.version):
        error(args.version + ' is not valid SemVer')
    
    if args.version not in tags:
        error('Version ' + args.version + ' not in history')

    if args.cache:
        args.cache = os.path.abspath(args.cache)
        
    runner = runtests.TestRunner(
        args.test_dir, 
        repo=repo, 
        cache=args.cache
    )

    tests = list(cvt(runner, tags, args.test_version))

    if args.cache:
        if not os.path.isdir(args.cache):
            os.makedirs(args.cache)
    
        # in parallel
        from multiprocessing import Pool
        pool = Pool()

        for i in pool.imap_unordered(setup_test, tests):
            print "Setup", i

    if not args.setup_only:
        for (runner, impl, test) in tests:
            for violation in runner.run(impl, test, args.test_suite):
                print "V{},{},{},{!r}".format(args.test_version, *violation)

def error(msg=None):
    if msg:
        print 'Error: ' + msg
    exit(1)

if __name__ == "__main__":
    main()
