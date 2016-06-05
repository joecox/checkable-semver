#!/bin/bash

versions=" \
1.0.0 \
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

function go {
    version=$1
    suite=$2
    log=$3

    if [ ! -e $log ]
    then
        tmp=$(mktemp)
        ./detect $version -r mocha -d test -s $suite --cache cache/$version |\
            grep -v '^Setup' > $tmp
        mv $tmp $log
    fi
}

N=0
for version in $versions
do
    printf -v NStr "%03d" $N
    if [ -e cache/$version ]
    then
        echo "test baby test baby $version"
        go $version jsapi results/eval/violations-jsapi-$NStr-$version.txt
        go $version all results/eval/violations-all-$NStr-$version.txt
    fi
    N=$((N+1))
done

cat results/eval/violations-jsapi-*.txt > results/eval/violations-jsapi.txt
cat results/eval/violations-all-*.txt > results/eval/violations-all.txt
