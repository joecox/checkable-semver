#!/bin/bash


file=./results/eval/violations.txt

versions=" \
V1.0.1 \
V1.0.2 \
V1.0.3 \
V1.1.0 \
V1.2.0 \
V1.2.1 \
V1.2.2 \
V1.3.0 \
V1.3.1 \
V1.3.2 \
V1.4.0 \
V1.4.1 \
V1.4.2 \
V1.5.0 \
V1.6.0 \
V1.7.0 \
V1.7.1 \
V1.7.2 \
V1.7.3 \
V1.7.4 \
V1.8.0 \
V1.8.1 \
V1.8.2 \
V1.9.0 \
V1.10.0 \
V1.11.0  \
V1.12.0 \
V1.12.1 \
V1.13.0 \
V1.14.0 \
V1.15.0 \
V1.15.1 \
V1.16.0 \
V1.16.1 \
V1.16.2 \
V1.17.0 \
V1.17.1 \
V1.18.0 \
V1.18.1 \
V1.18.2 \
V1.19.0 \
V1.20.0 \
V1.20.1 \
V1.21.0 \
V1.21.1 \
V1.21.2 \
V1.21.3 \
V1.21.4 \
V1.21.5 \
V2.0.0 \
V2.0.1 \
V2.1.0 \
V2.2.0 \
V2.2.1 \
V2.2.2 \
V2.2.3 \
V2.2.4 \
V2.2.5 \
V2.3.0 \
V2.3.4 \
Vv2.3.1 \
Vv2.3.2 \
Vv2.3.3 \
Vv2.4.1 \
Vv2.4.2 \
Vv2.4.3 \
Vv2.4.4 \
Vv2.4.5 \
Vv2.5.0 \
Vv2.5.1 \
Vv2.5.2 \
Vv2.5.3"

collector=`mktemp -t coll`
for version in $versions
do
    violations=`mktemp -t viol-$version`
    collectorNext=`mktemp -t coll`

    grep "$version" "$file" | sed "s/^[^'\"]*,//" | sort > "$violations"
    numver=`wc -l "$violations" | awk '{print $1}'`
    sort -m "$violations" "$collector" | uniq >"$collectorNext"
    uniqver=`cat "$violations" | uniq | wc -l | awk '{print $1}'`
    uniqcul=`cat "$collectorNext" | uniq | wc -l | awk '{print $1}'`

    collector="$collectorNext"

    echo "${version:1} $numver $uniqver $uniqcul"
done
