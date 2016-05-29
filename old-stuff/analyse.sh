
# This file performs some analyses the out folder. 
# Create the outfolder using the testall.sh script.

folder=$1

if [ ! -e tests.txt ]
then
    tests=$(find $folder -type f -exec cat {} \; | \
        sed -n -E "s/(ok|not ok) [0-9]+ +([^#]*).*$/\2/p" | \
        sort | uniq)

    echo "$tests" > tests.txt
else
    tests=$(cat tests.txt)
fi

if [ ! -e analysis ] 
then
    mkdir -p analysis
    testid=0
    echo "$tests" | while read test
    do
        filename="analysis/$(printf "%04d.csv" $testid)"
        echo -n "$filename: "
        echo "$test"
        find $folder -type f -exec grep -H "$test" {} \; | \
            sed -e "s/out\///" -e "s/[\/,:]/,/g" | \
            sed -E -e "s/(not ok|ok).*/\1/" \
                   -e "s/not ok/0/" -e "s/ok/1/" \
            > "$filename"
        ((testid+=1))
    done
fi

for test in $(find analysis -type f -not -name '*.table.*')
do
    echo "$test"
    newname=${test%.csv}.table.csv
    python3 table.py < $test > $newname
    python3 table2img.py $newname
done



