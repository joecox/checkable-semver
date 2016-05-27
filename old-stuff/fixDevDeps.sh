#!/bin/bash

devDeps=$(json -f mocha-1.0.0/package.json devDependencies)

for d in mocha-*
do
    json -I -f $d/package.json -e "this.devDependencies=$devDeps"
    (cd $d; npm install)
done
