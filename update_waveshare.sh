#!/bin/bash
# wavehsare repo
WS_REPO="https://github.com/waveshare/e-Paper.git"
WS_ROOT="e-Paper"
WS_LIB_PATH="RaspberryPi_JetsonNano/python/lib/waveshare_epd"

PROJECT="./paperpi/"
WS_LOCAL="$PROJECT/waveshare_epd"

# git clone into temporary directory
WS_TEMP=$(mktemp -d -t waveshare_XXXXX)

git clone $WS_REPO $WS_TEMP
if [[ $? -ne 0 ]]; 
then
  echo "failed to clone $WS_REPO"
  echo "see $WS_TEMP"
  exit 1
fi

WS_VERSION=$(git --git-dir $WS_TEMP/.git log -1 --format=%h\ %ci)
echo "this verison is: $WS_VERSION"

rm -r $WS_LOCAL.ignore
mv $WS_LOCAL $WS_LOCAL.ignore
cp -r $WS_TEMP/$WS_LIB_PATH $PROJECT

# add the latest commit to the constants file for record keeping
sed -i "s#\(ws_version\s\?=\).*#\1 '$WS_VERSION'#g" $PROJECT/my_constants.py


### Patch issues with WaveShare Modules ###
# remove uneeded numpy imports in waveshare modules
## Patch issues with WaveShare Modules ##
# remove unneeded numpy imports in waveshare modules
find $WS_LOCAL -type f -exec sed -i 's/^import numpy/#&/' {} \;

# add default value to `update` arg in init() method
find $WS_LOCAL -type f -exec sed -i -E 's/(^\W+def init\(self,\W+update)/\1=False/g' {} \;

# add default value to `color` arg in Clear() method (see epd2in7 for example)
find $WS_LOCAL -type f -exec sed -i -E 's/(\W+def Clear\(self,\W+color)\)/\1=0xFF)/' {} \;

# default to full update in def init() for screens that support partial update
echo "set default lut value in init()"
find $WS_LOCAL -type f -exec sed -i -E 's/(def init\(self, lut)(.*)/\1=None\2\n        if not lut:\n            lut = self.lut_full_update/' {} \;
