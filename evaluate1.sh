#!/bin/bash

set -e

mochaUrl="git@github.com:mochajs/mocha.git"

outdir="$1"
seq="$(echo $2 | cut -d, -f 1)"
# 0-pad seq
printf -v seq "%05d" $seq

tag="$(echo $2 | cut -d, -f 2)"
violations="$outdir/violations-seq-$seq.txt"

tooldir=$(pwd)
tmpdir=$(mktemp -d)
git clone $mochaUrl $tmpdir

echo "Testing version $tag in $tmpdir"

pushd $tmpdir
$tooldir/detect -d test $tag -s all | tee -a "$violations"
popd

rm -rf $tmpdir
