#!/bin/bash

# assume: we are in the source dir, clean version of baseline mofo.

mochaUrl="git@github.com:mochajs/mocha.git"

versions="1.21.0 1.20.0 1.19.0 1.18.0 1.17.0 \
          1.16.0 1.15.0 1.14.0 1.13.0 1.12.0 \
          1.11.0 1.10.0 1.9.0 1.8.0 1.7.0 \
          1.6.0 1.5.0 1.4.0 1.3.0 1.2.0 1.1.0"

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
1.11.0 \
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
"

function testVersion {
    ver=$1
    echo "--------------------------------------------------"
    echo "Testing version $ver"
    echo "--------------------------------------------------"

    if [ -d "mocha-$ver" ]
    then
        cd "mocha-$ver"
    else
        git clone $mochaUrl "mocha-$ver"
        cd "mocha-$ver"
        git checkout $ver
        npm install
        git checkout 1.0.0 test
    fi

    if [ ! -e test.log ]
    then
        make test &> test.log
    fi
    
    cat test.log | sed -r "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]//g" | sed -n '/^\s*[0-9]* \(passing\|failing\|failed\)/p'
    cat test.log | sed -r "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]//g" | egrep 'passing|failing|failed' -A 10000 | sed -n '/^  [0-9]*) /p' | sed 's/^  [0-9]*) //'

    cd ..
}

#

for ver in $versions
do
  testVersion $ver
done
