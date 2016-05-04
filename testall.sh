# Execute me inside a repository with moca tests. 
# requires semver to work:
# >> npm i -g semver

testfolder=$1
outfolder=$2

mkdir -p "${outfolder}"

tags=`git tag --list`

base=1.0.0

for tag in $(semver -r "1" $tags)
do
    echo "Running on version: ${tag}"
    git reset --hard "${tag}"
    
    echo "Clean repository"
    git clean -dxf 
    
    echo "Installing packages" 
    npm install 

    echo "Checking out ${testfolder} at ${base}"
    rm -r "${testfolder}"
    git checkout ${base} -- "${testfolder}"

    echo "Running tests" 
    mocha --reporter=tap ${testfolder} | tee "${outfolder}/${tag}" | sed -n '/^#/p'
done
