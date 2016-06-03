#!/bin/bash

file=./results/eval/violations.txt

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

outfolder=./report/graphics/

outfile=$outfolder/violations.txt

rm -f $outfile

#collector=`mktemp -t coll`
for version in $versions
do
#    collectorNext=`mktemp -t coll`
    violations=`mktemp -t viol-$version`
    breaking=`mktemp -t breaking-$version`
    features=`mktemp -t features-$version`

    grep "V$version" "$file" > "$violations"

    grep -E "^[^,]+,[^,]+,$version" "$violations" | sed "s/^[^'\"]*,//" | sort > "$features"
    grep -E "^[^,]+,$version" "$violations" | sed "s/^[^'\"]*,//" | sort > "$breaking"

    # breaking_viol=`wc -l "$breaking" | awk '{print $1}'`
    # features_viol=`wc -l "$features" | awk '{print $1}'`
    
    #sort -m "$violations" "$collector" | uniq >"$collectorNext"
    #uniqcul=`cat "$collectorNext" | uniq | wc -l | awk '{print $1}'`
    #collector="$collectorNext"
    
    uniq_breaking_viol=`uniq "$breaking" | wc -l | awk '{print $1}'`
    uniq_feature_viol=`uniq "$features" | wc -l | awk '{print $1}'`

    echo "$version $uniq_breaking_viol $uniq_feature_viol $((uniq_feature_viol + uniq_breaking_viol))" >> $outfile
done
