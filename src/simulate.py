#!/usr/bin/env python2.7

import argparse
import logging

import git
import semver
import simtag

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--strict", action="store_true",
                   help="Run the simulation with strict bumping")
    p.add_argument("--repository", "-r",
                   help="Path to repository on the system.")
    p.add_argument("--verbose", "-v", action="count")

    args = p.parse_args()

    if args.verbose == 1:
        logging.basicConfig(level=logging.INFO)
    if args.verbose == 2:
        logging.basicConfig(level=logging.DEBUG)

    tags = [
        "1.0.1", "1.0.2", "1.0.3", "1.1.0", "1.2.0", "1.2.1", "1.2.2",
        "1.21.2", "1.21.3", "1.21.4", "1.21.5", "1.3.0", "1.3.1", "1.3.2",
        "1.4.0", "1.4.1", "1.4.2", "1.5.0", "1.6.0", "1.7.0", "1.7.1", "1.7.2",
        "1.7.3", "1.7.4", "1.8.0", "1.8.1", "1.8.2", "1.9.0", "1.10.0",
        "1.11.0", "1.12.0", "1.12.1", "1.13.0", "1.14.0", "1.15.0", "1.15.1",
        "1.16.0", "1.16.1", "1.16.2", "1.17.0", "1.17.1", "1.18.0", "1.18.1",
        "1.18.2", "1.19.0", "1.20.0", "1.20.1", "1.21.0", "1.21.1", "2.0.0",
        "2.0.1", "2.1.0", "2.2.0", "2.2.1", "2.2.2", "2.2.3", "2.2.4", "2.2.5",
        "2.3.0", "v2.3.1", "v2.3.2", "v2.3.3", "2.3.4", "v2.4.1", "v2.4.2",
        "v2.4.3", "v2.4.4", "v2.4.5", "v2.5.0", "v2.5.1", "v2.5.2", "v2.5.3"
    ]

    tags = semver.sort(tags)

    repo = git.Repository(args.repository)

    if not repo.is_repo():
        error("Not currently in a git repository")

    # actual2sim = { "1.0.0": "1.0.0" }
    sim2actual = { "1.0.0": "1.0.0" }
    
    sim_tags = [ "1.0.0" ]

    last_sim_tag = "1.0.0"
    last_actual_tag = "1.0.0"
    
    for actual_tag in tags:
        logging.info("Actual tag: %s", actual_tag)
        next_tag = simtag.next_tag(actual_tag, sim_tags, sim2actual, repo)

        if args.strict:
            if semver.cmp(actual_tag, next_tag) == 1: # v1 < v2
                logging.info("actual greater, bump to %s", actual_tag)
                next_tag = actual_tag
            else:
                actual_diff = semver.diff(last_actual_tag, actual_tag)
                if actual_diff > semver.diff(last_sim_tag, next_tag):
                    if actual_diff == 3:
                        next_tag = semver.bump_major(last_sim_tag)
                        logging.info("actual did major, bump to %s", next_tag)
                    elif actual_diff == 2:
                        next_tag = semver.bump_minor(last_sim_tag)
                        logging.info("actual did minor, bump to %s", next_tag)                                
        logging.info("Next tag: %s", next_tag)
        sim_tags.append(next_tag)
        sim2actual[next_tag] = actual_tag

        last_actual_tag = actual_tag
        last_sim_tag = next_tag
    
    print sim_tags
    
if __name__ == "__main__":
    main()
    

    
