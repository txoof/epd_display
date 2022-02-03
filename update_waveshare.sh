#!/bin/bash
# waveshare repo
ws_epd_git="https://github.com/waveshare/e-Paper.git"

# root within repo 
ws_root="e-Paper"
# location of python libraries
ws_library_path="e-Paper/RaspberryPi_JetsonNano/python/lib/waveshare_epd"

# project waveshare_epd path
project="./paperpi/"
ws_local="$project/waveshare_epd"



# create temporary directory
ws_tmp=$(mktemp -d -t waveshare_XXXXX)
pushd $ws_tmp
git clone $ws_epd_git
if [ $? -ne 0 ]; then
  echo "failed to clone $ws_epd_git"
  echo "see $ws_tmp"
  echo "exiting"
  exit 1
else
  pushd $ws_root
fi

echo ws_temp = $ws_tmp

# get the latest commit and store it
ws_version=$(git log -1 --format=%h\ %ci)
echo "this version is: $ws_version"
popd
popd

# backup the current version of the library
rm -r $ws_local.ignore
mv $ws_local $ws_local.ignore
cp -r $ws_tmp/$ws_library_path $project
# add the latest commit to the constants file for record keeping (?)
sed -i "s#\(ws_version\s\?=\).*#\1 '$ws_version'#g" $project/my_constants.py


### Patch issues with WaveShare Modules ###
# remove uneeded numpy imports in waveshare modules
find $ws_local -type f -exec sed -i 's/^import numpy/#&/' {} \;

# add default value to `update` arg in init() method
find $ws_local -type f -exec sed -i -E 's/(^\W+def init\(self,\W+update)/\1=False/g' {} \;
# add default value to `color` arg in Clear() method (see epd2in7 for example)
find $ws_local -type f -exec sed -i -E 's/(^\W+def Clear\(self,\W+color)/\1=0xFF/g' {} \; 

exit 0
