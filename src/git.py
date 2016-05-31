import os
from subprocess import call, Popen, PIPE

import semver

def clone(src, dest):
    call(["git", "clone", "--quiet", src, dest])

def is_repo():
    dir = os.getcwd()
    with open(os.devnull, 'w') as FNULL:
        return not call(["git", "rev-parse", "--git-dir"],
                        stdout=FNULL, stderr=FNULL)

def get_previous_tag():
    p = Popen(["git", "describe", "--abbrev=0", "--tags"], stdout=PIPE, stderr=PIPE)
    t, _ = p.communicate()
    t = t.strip()

    p = Popen(["git", "rev-list", "-n", "1", t], stdout=PIPE, stderr=PIPE)
    h, _ = p.communicate()
    h = h.strip()

    v = get_current_rev()
    if h != v:
        return t
    else:
        tags = get_tags()
        prev_t = tags[tags.index(t)-1]
        return prev_t

def co_by_tag(tag, files):
    with open(os.devnull, 'w') as FNULL:
        call(["git", "checkout", "tags/" + tag, "--", files])

def reset_hard(tag_or_rev):
    with open(os.devnull, 'w') as FNULL:
        call(["git", "reset", "--hard", tag_or_rev],
             stdout=FNULL)

def get_current_rev():
    p = Popen(["git", "rev-parse", "HEAD"], stdout=PIPE, stderr=PIPE)
    h, _ = p.communicate()
    return h.strip()

def get_current_branch():
    p = Popen(["git", "rev-parse", "--abbrev-ref", "HEAD"], stdout=PIPE, stderr=PIPE)
    b, _ = p.communicate()
    return b.strip()

def get_tags():
    p = Popen(["git", "tag", "-l"], stdout=PIPE, stderr=PIPE)
    tags, _ = p.communicate()
    return semver.sort(tags.strip().split("\n"))
