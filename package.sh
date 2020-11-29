#!/bin/bash
appName="paperpi"

version=`cat $appName/constants.py | sed -ne 's/^version\W\{0,\}=\W\{0,\}\(.*\)["'"'"']/\1/p'`
echo version number is $version
filename=$appName\_$version.tgz
latestName=$appName\_latest.tgz

case $1 in
  -r|--release)
    release=1
    build=1
    package=1
    ;;
  -p|--package)
    release=0
    build=0
    package=1
    ;;
  -b|--build)
    release=0
    build=1
    package=0
    ;;
  *)
    echo "useage: $0 [OPTION...]
      --package, -p: package only
      --build, -b: build only
      --release, -r: build, package and push the build to github"
    exit
    ;;
esac

echo $filename

if [[ $build -eq 1 ]]; then
  ./build.sh
#  pipenv run pyinstaller --clean --noconfirm slimpi.spec
fi

if [[ $package -eq 1 ]]; then

  tar cvzf $filename --transform 's,^,slimpi/,' -T manifest.txt
  cp $filename $latestName
fi


if [[ $release -eq 1 ]]; then
#  git add $filename
  git commit -m "update build" $latestName
  git push
fi

