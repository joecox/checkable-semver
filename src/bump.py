#!/usr/bin/env python

import argparse
import os
import shutil
from subprocess import call, Popen, PIPE
import tempfile
import re
import sys

import git
import semver

api_dir = None
repo_dir = None
rev = None
args = None
outf = None
viol_long_f = None

FNULL = open(os.devnull, 'w')

def main():
    global api_dir, repo_dir, rev, args, outf, viol_long_f
    
    p = argparse.ArgumentParser()
    p.add_argument("--dir", "-d", required=True,
                   help="The folder in which the api tests reside.")
    p.add_argument("test_version",
                   help="A version to test bumping to.")
    p.add_argument("--outdir", "-o",
                   help="Directory to store results.")
    p.add_argument("--test-script", "-t",
                   help="Shell script to run tests.")
    p.add_argument("--verbose", "-v", action="store_true",
                   help="Run with verbose output.")
    p.add_argument("--report-violations", action="store_true",
                   help="Report violation information")
    
    args = p.parse_args()

    if not git.is_repo():
        error("Not currently in a git repository")

    if git.get_current_branch() != "master":
        print git.get_current_branch()
        error("Must be on the master branch")

    if args.outdir:
        outf = open(os.path.join(args.outdir, 'out.log'), 'w')
        
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

    if args.report_violations and args.test_version:
        report_file = open(os.path.join(args.outdir, "violations-short.txt"), 'w')
        viol_long_f = open(os.path.join(args.outdir, "violations-long.txt"), 'w')
        
        diff = semver.diff(last_t, args.test_version)
        f_viol, b_viol = dv(tags, args.test_version)
        report_file.write(args.test_version + "," + str(len(f_viol) + len(b_viol)) + '\n')
    else:
        # First try bumping patch

        patch_v = semver.bump_patch(last_t)
        if args.verbose:
            print "Trying to bump to patch version " + patch_v
    
        patch_viol = dv(tags, patch_v)

        if not patch_viol:
            if args.verbose:
                print "Lowest safe version: " + patch_v
            else:
                print patch_v
        else: # try minor bump
            minor_v = semver.bump_minor(last_t)
            if args.verbose:
                print "Trying to bump to minor version " + minor_v

            minor_viol = dv(tags, minor_v)

            if not minor_viol:
                if args.verbose:
                    print "Lowest safe version: " + minor_v
                else:
                    print minor_v
            else: # Gotta do major bump
                if args.verbose:
                    print "Lowest safe version: " + semver.bump_major(last_t)
                else:
                    print semver.bump_major(last_t)

    if outf:
        outf.close()
    FNULL.close()

def dv(prev_v, v):
    in_minor_v = semver.get_prev_in_minor(prev_v, v)
    in_major_v = semver.get_prev_in_major(prev_v, v)
        
    f_viol = []
    b_viol = []

    api_dirname = os.path.basename(api_dir)

    for patch_v in in_minor_v:
        if args.verbose:
            print "Testing implementation version " + patch_v + " against current tests."

        tmp_dir = setup_repo(patch_v)

        # remove test folder from impl version
        testdir = os.path.join(tmp_dir, api_dirname)
        shutil.rmtree(testdir)
        # copy current tests to current impl folder
        shutil.copytree(api_dir, testdir)

        viol = test(patch_v, rev[0:6], testdir, tmp_dir)
        if viol:
            f_viol.append(viol)

        os.chdir(repo_dir)
        shutil.rmtree(tmp_dir)

    # setup current impl version
    tmp_dir = setup_repo()
            
    for minor_v in in_major_v:
        if args.verbose:
            print "Testing current rev " + rev[0:6] + " against test version " + minor_v

        # Remove and checkout test dir
        testdir = os.path.join(tmp_dir, api_dirname)
        shutil.rmtree(testdir)
        os.chdir(tmp_dir)
        git.co_by_tag(minor_v, api_dirname)
        os.chdir(repo_dir)
        
        viol = test(rev[0:6], minor_v, testdir, tmp_dir)
        if viol:
            b_viol.append(viol)

    os.chdir(repo_dir)
    shutil.rmtree(tmp_dir)
    
    return f_viol, b_viol

def test(impl_v, test_v, testdir, tmp_dir):
    if args.verbose:
        print "Running mocha tests of " + test_v + " on " + impl_v

    if args.test_script:
        os.chdir(tmp_dir)
        p = Popen(args.test_script.split(" "), stdout=PIPE, stderr=PIPE)
        o, e = p.communicate()
    else:
        p = Popen(["mocha", "--reporter=tap", testdir], stdout=PIPE, stderr=PIPE)
        o, e = p.communicate()

    if outf:
        if args.test_version:
            if impl_v == rev[0:6]:
                impl_v = args.test_version
            elif test_v == rev[0:6]:
                test_v = args.test_version
            outf.write('impl: ' + impl_v + ', test: ' + test_v + '\n')
    
    if args.test_script: # parse spec reporter
        errpat = "^\s*\d*\) (?P<err>.*):"
        m = re.findall(errpat, e, re.M)

        if not m:
            if outf:
                outf.write('  all tests passed\n')
            return []
        else:
            if outf:
                outf.write('  ' + '\n  '.join(m) + '\n')
            if viol_long_f:
                for viol in m:
                    viol_long_f.write('I' + impl_v + ',T' + test_v + ',V' + viol + '\n')
            return m
                

        
    # else: # parse tap reporter
    #     m = re.search('# fail (?P<numfailed>\d*)', o)
        
    # if m:
    #     if int(m.group("numfailed")) == 0:
    #         return
    #     else:
    #         print "Violations found!"
    #         return m.group("numfailed")
    # else:
    #     print o, e
    #     error("re search failed")

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
    if args.verbose:
        print tag + ": " + "Installing npm dependencies..."

    call(["json", "-I", "-f", "package.json", "-e", "this.devDependencies.should='<2'"])
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
