#!/bin/bash

# fix the dependency on "should" package
json -I -f mocha-1.0.0/package.json -e 'this.devDependencies.should="<2"'

devDeps=$(json -f mocha-1.0.0/package.json devDependencies)

for d in mocha-*
do
    json -I -f $d/package.json -e "this.devDependencies=$devDeps"
    (cd $d; npm install)
done
