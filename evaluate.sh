#!/bin/bash

mochaUrl="git@github.com:mochajs/mocha.git"

tooldir=`pwd`

tmpdir=`mktemp -d`

git clone $mochaUrl $tmpdir

cd $tmpdir

tags=`git tag --list`

versions=" \
1.0.1 \
1.0.2 \
1.0.3 \
1.1.0 \
1.2.0 \
1.2.1 \
1.2.2 \
1.3.0 \
1.3.1 \
1.3.2 \
1.4.0 \
1.4.1 \
1.4.2 \
1.5.0 \
1.6.0 \
1.7.0 \
1.7.1 \
1.7.2 \
1.7.3 \
1.7.4 \
1.8.0 \
1.8.1 \
1.8.2 \
1.9.0 \
1.10.0 \
1.11.0  \
1.12.0 \
1.12.1 \
1.13.0 \
1.14.0 \
1.15.0 \
1.15.1 \
1.16.0 \
1.16.1 \
1.16.2 \
1.17.0 \
1.17.1 \
1.18.0 \
1.18.1 \
1.18.2 \
1.19.0 \
1.20.0 \
1.20.1 \
1.21.0 \
1.21.1 \
1.21.2 \
1.21.3 \
1.21.4 \
1.21.5 \
2.0.0 \
2.0.1 \
2.1.0 \
2.2.0 \
2.2.1 \
2.2.2 \
2.2.3 \
2.2.4 \
2.2.5 \
2.3.0 \
2.3.4 \
v2.3.1 \
v2.3.2 \
v2.3.3 \
v2.4.1 \
v2.4.2 \
v2.4.3 \
v2.4.4 \
v2.4.5 \
v2.5.0 \
v2.5.1 \
v2.5.2 \
v2.5.3"

outdir=results/eval
mkdir -p $outdir
touch $tooldir/$outdir/tags.txt
touch $tooldir/$outdir/violations.txt
touch $tooldir/$outdir/violations-verbose.txt

echo "" > $tooldir/$outdir/violations.txt
echo "" > $tooldir/$outdir/violations-verbose.txt

for tag in $versions
do
    echo "--------------------------------------------------"
    echo "Testing version $tag"
    echo "--------------------------------------------------"

    cd $tmpdir

    $tooldir/bump -d test --test-script "make test-jsapi" $tag -o $tooldir/$outdir/ --report-violations -v

    cat $tooldir/$outdir/violations-short.txt >> $tooldir/$outdir/violations.txt
    cat $tooldir/$outdir/violations-long.txt >> $tooldir/$outdir/violations-verbose.txt
    
#    echo "" > $tooldir/$outdir/tags.txt
#    echo "Actual tag: $tag, suggested tag: $suggested_tag" >> $tooldir/$outdir/tags.txt

#    echo "is: $tag should: $suggested_tag"
done

rm $tooldir/$outdir/violations-short.txt


    
    
