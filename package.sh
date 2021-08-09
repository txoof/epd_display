#!/bin/bash
appName="paperpi"

version=`cat $appName/my_constants.py | sed -ne 's/^version\W\{0,\}=\W\{0,\}\(.*\)["'"'"']/\1/p'`
echo version number is $version
filename=$appName\_$version.tgz
latestName=$appName\_latest.tgz

release=0
build=0
package=0

case $1 in
  -r|--release)
    release=$((release+1))
    build=$((build+1))
    package=$((package+1))
    ;;
  -p|--package)
    package=$((package+1))
    ;;
  -b|--build)
    build=$((build+1))
    ;;
  *)
    echo "useage: $0 [OPTION...]
      --package, -p: package only
      --build, -b: build only
      --release, -r: build, package update documents and push the build to github"
    exit
    ;;
esac

echo $filename

if [[ $build -eq 1 ]]; then
  ./build.sh
fi

if [[ $package -eq 1 ]]; then

  tar hcvzf $filename --transform 's,^,paperpi/,' -T manifest.txt
  cp $filename $latestName
fi


if [[ $release -eq 1 ]]; then
#  git add $filename
  pipenv run python create_docs.py
  git commit -m "update documentation" ./paperpi/plugins/*.md ./documentation/*.md
  git commit -m "update build" $latestName
  git tag -a "v$version" -m "release version: $version"
  git push
fi

