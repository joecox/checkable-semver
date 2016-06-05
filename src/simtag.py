#!/usr/bin/env python2.7

import argparse
import logging
import os

import git
import semver
import runtests

def next_tag(actual_tag, sim_tags, sim2actual, repo):
    last_tag = sim_tags[-1]

    runner = runtests.TestRunner(
        "test",
        repo=repo,
        cache="out/cache-"+actual_tag
    )

    nf_viol, bc_viol = dv(runner, sim_tags, actual_tag,
                          semver.bump_patch(last_tag), sim2actual)
    if not nf_viol and not bc_viol:
        return semver.bump_patch(last_tag)
    elif not bc_viol:
        return semver.bump_minor(last_tag)
    else:
        return semver.bump_major(last_tag)


def dv(runner, history, actual_tag, new_tag, sim2actual):
    in_minor_v = semver.get_prev_in_minor(history, new_tag)
    in_major_v = semver.get_prev_in_major(history, new_tag)

    new_feature_violations = []
    backward_compat_violations = []
    for patch_v in in_minor_v:
        logging.info("Test sim: impl " + patch_v + ", test " + new_tag)
        new_feature_violations.extend(
            runner.run(sim2actual[patch_v], actual_tag, "jsapi")
        )

    for minor_v in in_major_v:
        logging.info("Test sim: impl " + new_tag + ", test " + minor_v)
        backward_compat_violations.extend(
            runner.run(actual_tag, sim2actual[minor_v], "jsapi")
        )

    return new_feature_violations, backward_compat_violations

