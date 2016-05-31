#!/usr/bin/env python

import argparse
import os
import shutil
from subprocess import call, Popen, PIPE
import tempfile
import re

import git
import semver

api_dir = None
repo_dir = None
rev = None
args = None
outf = None

FNULL = open(os.devnull, 'w')

def main():
    global api_dir, repo_dir, rev, args, outf
    
    p = argparse.ArgumentParser()
    p.add_argument("--dir", "-d", required=True,
                   help="The folder in which the api tests reside.")
    p.add_argument("--test-version",
                   help="A version to test bumping to.")
    p.add_argument("--outfile", "-o",
                   help="Print out any semver violations.")
    p.add_argument("--test-script", "-t",
                   help="Shell script to run tests.")

    args = p.parse_args()

    if not git.is_repo():
        error("Not currently in a git repository")

    if git.get_current_branch() != "master":
        print git.get_current_branch()
        error("Must be on the master branch")

    if args.outfile:
        outf = open(args.outfile, 'w')
        
    repo_dir = os.getcwd()
    
    api_dir = os.path.abspath(args.dir)
    if not os.path.isdir(api_dir):
        error(args.dir + " is either not a directory or does not exist.")


    tags = git.get_tags()

    if args.test_version:
        if not semver.valid(args.test_version):
            error(args.test_version + ' is not valid SemVer')
        if args.test_version not in tags:
            error('Version ' + args.test_version + ' not in history')

    # If args.test_version has been set, reset to it
    if args.test_version:
        git.reset_hard(args.test_version)
    # Else continue on current commit
    
    last_t = git.get_previous_tag()
    rev = git.get_current_rev()
    
    # First try bumping patch

    patch_v = semver.bump_patch(last_t)
    print "Trying to bump to patch version " + patch_v
    
    patch_viol = dv(tags, patch_v)

    if not patch_viol:
        print "Lowest safe version: " + patch_v
    else: # try minor bump
        minor_v = semver.bump_minor(last_t)
        print "Trying to bump to minor version " + minor_v
        
        minor_viol = dv(tags, minor_v)

        if not minor_viol:
            print "Lowest safe version: " + minor_v
        else: # Gotta do major bump
            print "Lowest safe version: " + semver.bump_major(last_t)

    if outf:
        outf.close()
    FNULL.close()

def dv(prev_v, v):
    in_minor_v = semver.get_prev_in_minor(prev_v, v)
    in_major_v = semver.get_prev_in_major(prev_v, v)

    print in_minor_v
    print in_major_v
    error()
    
    violations = []

    api_dirname = os.path.basename(api_dir)

    for patch_v in in_minor_v:
        print "Testing implementation version " + patch_v + " against current tests."

        tmp_dir = setup_repo(patch_v)

        # remove test folder from impl version
        testdir = os.path.join(tmp_dir, api_dirname)
        shutil.rmtree(testdir)
        # copy current tests to current impl folder
        shutil.copytree(api_dir, testdir)

        viol = test(patch_v, rev[0:6], testdir)
        if viol:
            violations.append(viol)

        shutil.rmtree(tmp_dir)

    # setup current impl version
    tmp_dir = setup_repo()
            
    for minor_v in in_major_v:
        print "Testing current rev " + rev[0:6] + " against test version " + minor_v

        # Remove and checkout test dir
        testdir = os.path.join(tmp_dir, api_dirname)
        shutil.rmtree(testdir)
        os.chdir(tmp_dir)
        git.co_by_tag(minor_v, api_dirname)
        os.chdir(repo_dir)
        
        viol = test(rev[0:6], minor_v, testdir)
        if viol:
            violations.append(viol)

    shutil.rmtree(tmp_dir)
    
    return violations

def test(impl_v, test_v, testdir):
    print "Running mocha tests of " + test_v + " on " + impl_v

    if args.test_script:
        os.chdir(repo_dir)
        p = Popen(args.test_script.split(" "), stdout=PIPE, stderr=PIPE)
        o, e = p.communicate()
    else:
        p = Popen(["mocha", "--reporter=tap", testdir], stdout=PIPE, stderr=PIPE)
        o, e = p.communicate()
    
    if outf:
        outf.write(o)

    if args.test_script:
        m = re.search('(?P<numfailed>\d*) failing', o)
        if not m:
            return
    else:
        m = re.search('# fail (?P<numfailed>\d*)', o)
        
    if m:
        if int(m.group("numfailed")) == 0:
            return
        else:
            print "Violations found!"
            return m.group("numfailed")
    else:
        print o, e
        error("re search failed")

def setup_repo(tag=None):
    tmp_dir = tempfile.mkdtemp()

    git.clone(repo_dir, tmp_dir)
    os.chdir(tmp_dir)
    if tag:
        git.reset_hard(tag)
    npminstall(tag)
    os.chdir(repo_dir)
    return tmp_dir

def npminstall(tag):
    if not tag:
        tag = rev[0:6]
    print tag + ": " + "Installing npm dependencies..."
    call(["npm", "install"], stdout=FNULL, stderr=FNULL)

def error(msg=None):
    global FNULL
    if msg:
        print 'Error: ' + msg
    if outf:
        outf.close()
    FNULL.close()
    exit(1)

if __name__ == "__main__":
    main()
