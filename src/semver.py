import re

VALID_SEMVER_RE = re.compile("v?(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-((?:(?:\d*[A-Za-z-][0-9A-Za-z-]*|(?:0|[1-9]\d*))\.)*(?:\d*[A-Za-z-][0-9A-Za-z-]*|(?:0|[1-9]\d*))))?(?:\+((?:(?:[0-9A-Za-z-]+)\.)*[0-9A-Za-z-]+))?")

def trim_version(v):
    return v.strip("v")

def sort(versions):
    return sorted(versions, cmp=cmp)

def cmp(v1, v2):
    # Assuming 'nat.nat.nat' at the moment
    if not valid(v1):
        raise ValueError(v1 + ' is not valid SemVer')
    if not valid(v2):
        raise ValueError(v2 + ' is not valid SemVer')

    m1 = parse(v1)
    m2 = parse(v2)

    for i in range(len(m1)):
        if m1[i] > m2[i]:
            return 1
        elif m1[i] < m2[i]:
            return -1

    return 0

def bump_major(v):
    m = parse(v)
    return "{}.{}.{}".format(m[0] + 1, 0, 0)

def bump_minor(v):
    m = parse(v)
    return "{}.{}.{}".format(m[0], m[1] + 1, 0)

def bump_patch(v):
    m = parse(v)
    return "{}.{}.{}".format(m[0], m[1], m[2] + 1)

def parse(v):
    m = VALID_SEMVER_RE.match(v)
    return [int(x) for x in [ m.group('major'), m.group('minor'), m.group('patch') ]]

def valid(v):
    if VALID_SEMVER_RE.match(v):
        return True
    else:
        return False

def diff(v1, v2):
    m1 = parse(v1)
    m2 = parse(v2)

    if m1[0] != m2[0]:
        return 3
    if m1[1] != m2[1]:
        return 2
    if m1[2] != m2[2]:
        return 1

    return 0

def get_prev(prev_v, cur_v, level):
    vs = []
    for v in prev_v:
        if diff(v, cur_v) <= level and cmp(v, cur_v) == -1:
            vs.append(v)

    return vs
    
def get_prev_in_minor(prev_v, cur_v):
    return get_prev(prev_v, cur_v, 1)

def get_prev_in_major(prev_v, cur_v):
    return get_prev(prev_v, cur_v, 2)
