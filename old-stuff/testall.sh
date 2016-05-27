# Execute me inside a repository with moca tests. 
# requires semver to work:
# >> npm i -g semver

testfolder=$1
outfolder=$2

mkdir -p "${outfolder}"

tags=`git tag --list`

versions=`semver -r "1" $tags`

for tag in $versions 
do
    tagfolder="${outfolder}/${tag}"
    mkdir -p "${tagfolder}"
    echo "Running on version: ${tag}"
    git reset --hard "${tag}"

    echo "Clean repository"
    git clean -dxf 

    echo "Installing packages" 
    npm install 

    for testv in $versions
    do
        echo "Checking out ${testfolder} at ${testv}"
        rm -r "${testfolder}"
        git checkout ${testv} -- "${testfolder}"

        echo "Running tests" 
        mocha --reporter=tap ${testfolder} | tee "${tagfolder}/${testv}" | sed -n '/^#/p'
    done
done
