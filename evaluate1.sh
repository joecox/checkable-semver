#!/bin/bash

set -e

mochaUrl="git@github.com:mochajs/mocha.git"

outdir="$1"
tag="$2"
violations="$outdir/violations-tag-$tag.txt"

tooldir=$(pwd)
tmpdir=$(mktemp -d)
git clone $mochaUrl $tmpdir

echo "Testing version $tag in $tmpdir"

pushd $tmpdir
$tooldir/bump -d test $tag | tee -a "$violations"
popd

rm -rf $tmpdir
