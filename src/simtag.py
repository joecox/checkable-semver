#!/usr/bin/env python2.7

import argparse
import logging
import os

import git
import semver
import runtests

def next_tag(actual_tag, sim_tags, sim2actual, repo, ignorelist):
    last_tag = sim_tags[-1]

    runner = runtests.TestRunner(
        "test",
        repo=repo,
        cache="out/cache-"+actual_tag
    )

    nf_viol, bc_viol = cvt(runner, sim_tags, actual_tag,
                           semver.bump_patch(last_tag), sim2actual, ignorelist)
    if not nf_viol and not bc_viol:
        return semver.bump_patch(last_tag)
    elif not bc_viol:
        return semver.bump_minor(last_tag)
    else:
        return semver.bump_major(last_tag)


def cvt(runner, history, actual_tag, new_tag, sim2actual, ignorelist):
    in_minor_v = semver.get_prev_in_minor(history, new_tag)
    in_major_v = semver.get_prev_in_major(history, new_tag)

    new_feature_violations = []
    backward_compat_violations = []
    for patch_v in in_minor_v:
        logging.info("Test sim: impl " + patch_v + ", test " + new_tag)
        for violation in runner.run(sim2actual[patch_v], actual_tag, "jsapi"):
            if violation[2] not in ignorelist:
                new_feature_violations.append(violation)
            else:
                logging.debug("Violation ignored")

    for minor_v in in_major_v:
        logging.info("Test sim: impl " + new_tag + ", test " + minor_v)
        for violation in runner.run(actual_tag, sim2actual[minor_v], "jsapi"):
            if violation[2] not in ignorelist:
                backward_compat_violations.append(violation)
            else:
                logging.debug("Violation ignored")

    return new_feature_violations, backward_compat_violations

