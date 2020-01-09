#!/bin/sh

BASEPATH=$(dirname "$0")
# export PATH=$PATH:$BASEPATH/USD:$BASEPATH/usdzconvert;
export PATH=$PATH:/usdz-exporter/USD:/usdz-exporter/usdzconvert;
export PYTHONPATH=$PYTHONPATH:$BASEPATH/USD/lib/python

FILE=""
DIR="/usdz-exporter/input"
OUTPUT="/usdz-exporter/output"
# init
# look for empty dir 
if [ "$(ls -A $DIR)" ]; then
  for file in $DIR/*; do
    name="$(basename -- $file)"
    usdzconvert $file $OUTPUT/${name%.glb}.usdz
    echo "${file##*/}"
  done
else
  echo "No files to convert"
fi
