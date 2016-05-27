#!/usr/bin/env python

import argparse
import os
import shutil
from subprocess import call, Popen, PIPE
import tempfile

import git
import semver

api_dir = None
tmp_dir = None

def main():
    global api_dir, tmp_dir
    
    p = argparse.ArgumentParser()
    p.add_argument("--dir", "-d", required=True,
                   help="The folder in which the api tests reside.")
    p.add_argument("--version", "-v",
                   help="A proposed version to bump to.")
    p.add_argument("--report-violations", "-r",
                   help="Print out any semver violations.")

    args = p.parse_args()

    if not git.is_repo():
        error("Not currently in a git repository")

    if git.uncommitted_changes():
        error("You have uncommitted changes!")

    if git.get_current_branch() != "master":
        print git.get_current_branch()
        error("Must be on the master branch")
        
    rev = git.get_current_rev()
    url = git.get_remote_url()

    repo_dir = os.getcwd()
    
    # For now we'll clone the repo in a temp dir
    tmp_dir = tempfile.mkdtemp()
    os.chdir(tmp_dir)
    git.clone(url, ".")
    git.reset_hard(rev)
        
    api_dir = os.path.abspath(args.dir)
    if not os.path.isdir(api_dir):
        error(args.dir + " is either not a directory or does not exist.")

    last_v = git.get_latest_version()

    if args.version:
        if not semver.valid(args.version):
            error(args.version + ' is not valid SemVer')
        if not semver.cmp(last_v, args.version) == -1:
            error(args.version + ' must be greater than previous version ' + last_v)

    tags = git.get_tags()

    # First try bumping patch
    patch_v = semver.bump_patch(last_v)
    patch_viol = dv(tags, patch_v, rev)

    if not patch_viol:
        print patch_v
    else: # try minor bump
        minor_v = semver.bump_minor(last_v)
        minor_viol = dv(tags, minor_v, rev)

        if not minor_viol:
            print minor_v
        else: # Gotta do major bump
            print semver.bump_major(last_v)

    shutil.rmtree(tmp_dir)

def dv(prev_v, v, rev):
    FNULL = open(os.devnull, 'w')
    
    in_minor_v = semver.get_prev_in_minor(prev_v, v)
    in_major_v = semver.get_prev_in_major(prev_v, v)

    violations = []

    # Save api_dir of current rev
    save_loc = tempfile.mkdtemp()
    call(["cp", "-r", api_dir, save_loc], stdout=FNULL, stderr=FNULL)

    api_rel = os.path.basename(api_dir)

    for patch_v in in_minor_v:
        print "Testing implementation version " + patch_v + " against current tests."
        git.reset_hard(patch_v)
        call(["npm", "install"], stdout=FNULL)
        shutil.rmtree(api_dir)
        call(["cp", "-r", os.path.join(save_loc, api_rel), "."], stdout=FNULL, stderr=FNULL)
        viol = test(patch_v, v)
        if viol:
            violations.append(viol)

    shutil.rmtree(save_loc)
    git.reset_hard(rev)
    call(["npm", "install"], stdout=FNULL)
            
    for minor_v in in_major_v:
        print "Testing current implementation against test version " + minor_v
        shutil.rmtree(api_dir)
        git.co_by_tag(minor_v, api_dir)
        
        viol = test(v, minor_v)
        if viol:
            violations.append(viol)

    FNULL.close()
             
    return violations

def test(impl_v, test_v):
    p = Popen(["mocha", "--reporter=tap", api_dir])
    # o, e = p.communicate()

def error(msg=None):
    global tmp_dir
    if msg:
        print 'Error: ' + msg
    if tmp_dir:
        shutil.rmtree(tmp_dir)
    exit(1)

if __name__ == "__main__":
    main()
