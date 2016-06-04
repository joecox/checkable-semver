import os
from subprocess import call, Popen, PIPE
import logging

import semver

def silent_do(args):
    with open(os.devnull, 'wb') as FNULL:
        return not call(args, stdout=FNULL, stderr=FNULL)

class Context:

    def __init__(self, directory):
        self.directory = directory

    def __enter__(self):
        self.context = os.path.abspath(os.getcwd())
        os.chdir(self.directory)
        logging.debug("Changed directory %s", os.getcwd())
        return self

    def __exit__(self, *args, **kwargs):
        os.chdir(self.context)
        logging.debug("Returned to %s", os.getcwd())


class Repository: 

    def __init__(self, directory):
        self.directory = os.path.abspath(directory);

    def in_context(self):
        return Context(self.directory)

    def do(self, *args):
        with self.in_context():
            cmd = ["git"]
            cmd.extend(args)
            logging.debug("Ran %s on %s ", cmd, self.directory)
            return silent_do(cmd)

    def reset(self, ref, hard=False):
        cmd = ["reset"]
        if hard:
            cmd.append("--hard")
        cmd.append(ref)
        return self.do(*cmd)

    def checkout(self, ref, files=[]):
        cmd = ["checkout", ref]
        if files:
            cmd.extend(["--"] + files)
        return self.do(*cmd)

    def is_repo(self):
        return self.do("rev-parse", "--git-dir")

    def clone(self, dest):
        clone(self.directory, dest);
        return Repository(dest)

def clone(src, dest):
    silent_do(["git", "clone", "--quiet", src, dest])

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
