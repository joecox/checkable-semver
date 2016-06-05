#!/usr/bin/env python

from subprocess import call, Popen, PIPE
import os
import re

def sh(cmd):
  with open(os.devnull, 'wb') as FNULL:
    p = Popen(cmd, stdout=PIPE, stderr=FNULL, shell=True)
    stdout, stderr = p.communicate()
    out = stdout.strip().split('\n')
    if out == ['']:
      return []
    else:
      return out
      

versions=sh("ls cache")

jsapi_tests={}
all_tests={}
jsapi_cvts={}
all_cvts={}
failed_jsapi_cvts={}
failed_all_cvts={}
for v in versions:
  jsapi_tests[v] = int(sh("""grep -E "^(ok|not ok)" results/eval/jsapi-tests-%s.txt | wc -l""" % v)[0])
  all_tests[v] = int(sh("""grep -E "^(ok|not ok)" results/eval/all-tests-%s.txt | wc -l""" % v)[0])
  jsapi_cvts[v] = 0
  all_cvts[v] = 0

  failed_jsapi_cvts[v] = int(sh("cat results/eval/violations-jsapi-*-%s.txt | wc -l" % v)[0])
  failed_all_cvts[v] = int(sh("cat results/eval/violations-all-*-%s.txt | wc -l" % v)[0])
  
for v in versions:
  for d in sh("ls cache/%s/" % v):
    mo = re.match("i(.*)-t(.*)", d)
    impl = mo.group(1)
    test = mo.group(2)

    try:
      jsapi_cvts[impl] += int(jsapi_tests[test])
    except:
      pass

    try:
      all_cvts[impl] += int(all_tests[test])
    except:
      pass

jsapi_pcts=[]
all_pcts=[]
    
for v in versions:
  try:
    pct_jsapi = float(failed_jsapi_cvts[v])/jsapi_cvts[v]
  except:
    pct_jsapi = 0
    
  try:
    pct_all = float(failed_all_cvts[v])/all_cvts[v]
  except:
    pct_all = 0

  # sometimes test-all fails, so jsapi ends up running more tests than all.
  # this skews the data, so filter these out.
  if jsapi_cvts[v] < all_cvts[v]:
    jsapi_pcts.append(pct_jsapi)
    all_pcts.append(pct_all)
    
  print "%s,%f,%s,%s,%f,%s,%s" % (v, pct_jsapi, failed_jsapi_cvts[v], jsapi_cvts[v], pct_all, failed_all_cvts[v], all_cvts[v])

def avg(l):
  return sum(l) / float(len(l))

avg_jsapi = avg(jsapi_pcts)
avg_all = avg(all_pcts)
print "Average jsapi: %s" % avg_jsapi
print "Average all: %s" % avg_all
print avg_all/avg_jsapi
