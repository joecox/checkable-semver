#!/usr/bin/env python
from subprocess import check_output
import sys
import os
import json

def dox(filename):
  # run dox on the javascript file, parse and return json output.
  return json.loads(check_output("dox < " + filename, shell=True))

def is_method(obj):
  try:
    # this property exists if the declaration is a method
    obj['ctx']['constructor']
    return (obj['ctx']['type'] == 'method')
  except:
    return False

def method_info(obj):
  if obj['isPrivate']:
    vis = "private"
  else:
    vis = "public"

  return (obj['ctx']['constructor'], obj['ctx']['name'], vis)


def lib_files(mocha_dir):
  cmd = "find %s/lib -name '*.js'" % mocha_dir
  out = check_output(cmd, shell=True)
  return out.split('\n')[:-1]

if __name__ == "__main__":
  mocha_dir = sys.argv[1]
  libfiles = lib_files(mocha_dir)
  for f in libfiles:
    for m in map(method_info, filter(is_method, dox(f))):
      print m
