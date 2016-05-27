import os
from subprocess import call, Popen, PIPE

import semver

def is_repo():
    dir = os.getcwd()
    with open(os.devnull, 'w') as FNULL:
        return not call(["git", "rev-parse", "--git-dir"],
                        stdout=FNULL, stderr=FNULL)

def get_latest_version():
    p = Popen(["git", "describe", "--abbrev=0"], stdout=PIPE, stderr=PIPE)
    v, _ = p.communicate()
    return v.strip()

def co_by_tag(tag, files):
    with open(os.devnull, 'w') as FNULL:
        call(["git", "checkout", "tags/" + tag, "--", files],
             stdout=FNULL)

def reset_hard(tag_or_rev):
    with open(os.devnull, 'w') as FNULL:
        call(["git", "reset", "--hard", tag_or_rev],
             stdout=FNULL)

def uncommitted_changes():
    return call(["git", "diff-index", "--quiet", "HEAD", "--"])

def get_current_rev():
    p = Popen(["git", "rev-parse", "HEAD"], stdout=PIPE, stderr=PIPE)
    h, _ = p.communicate()
    return h.strip()

def get_current_branch():
    p = Popen(["git", "rev-parse", "--abbrev-ref", "HEAD"], stdout=PIPE, stderr=PIPE)
    b, _ = p.communicate()
    return b.strip()

def get_remote_url():
    p = Popen(["git", "remote", "get-url", "origin"], stdout=PIPE, stderr=PIPE)
    u, _ = p.communicate()
    return u.strip()

def clone(url, dir):
    call(["git", "clone", "--quiet", url, dir])

def get_tags():
    p = Popen(["git", "tag", "-l"], stdout=PIPE, stderr=PIPE)
    tags, _ = p.communicate()
    return tags.strip().split("\n")
