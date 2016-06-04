#!/usr/bin/env python2.7

import argparse
import logging
import os

import git
import semver
import runtests

def main():
    p = argparse.ArgumentParser()
    p.add_argument("version", help="A tag or revision to bump to.")
    p.add_argument("--test-dir", "-d", required=True,
                   help="The folder in which the test suite resides.")
    p.add_argument("--repository", "-r",
                   help="Path to repository on the system, default is CWD.")
    p.add_argument("--cache", "-c",
                   help="A cache of results.")
    p.add_argument("--verbose", "-v", action="count",
                   help="Fun with verbose output.")
    p.add_argument("--test-suite", "-s", choices=["all", "unit", "jsapi"],
                   required=True,
                   help="The test suite to run.")
    
    args = p.parse_args()

    if args.verbose == 1:
        logging.basicConfig(level=logging.INFO)
    if args.verbose == 2:
        logging.basicConfig(level=logging.DEBUG)

    repo = git.Repository(args.repository)

    if not repo.is_repo():
        error("No git repository found")

    tags = semver.sort(repo.get_tags())
    last_tag = tags[tags.index(args.version)-1]

    if not semver.valid(args.version):
        error(args.version + " is not valid SemVer")

    if args.version not in tags:
        error("Version " + args.version + " not in history")

    if args.cache:
        args.cache = os.path.abspath(args.cache)

    runner = runtests.TestRunner(
        args.test_dir,
        repo=repo,
        cache=args.cache
    )

    nf_viol, bc_viol = dv(runner, args.test_suite, tags, args.version)
    if not nf_viol and not bc_viol:
        print semver.bump_patch(last_tag)
    elif not bc_viol:
        print semver.bump_minor(last_tag)
    else:
        print semver.bump_major(last_tag)


def dv(runner, suite, history, v):
    in_minor_v = semver.get_prev_in_minor(history, v)
    in_major_v = semver.get_prev_in_major(history, v)

    new_feature_violations = []
    backward_compat_violations = []
    for patch_v in in_minor_v:
        new_feature_violations.extend(runner.run(patch_v, v, suite))

    for minor_v in in_major_v:
        backward_compat_violations.extend(runner.run(v, minor_v, suite))

    return new_feature_violations, backward_compat_violations

if __name__ == "__main__":
    main()
