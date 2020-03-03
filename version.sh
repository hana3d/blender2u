#!/bin/bash
input="./__init__.py"
line=`sed "6q;d" $input`
version0=$(echo "${line:15:3}" | sed 's/[(, ]//g')
version1=$(echo "${line:19:3}" | sed 's/[, ]//g')
version2=$(echo "${line:22:3}" | sed 's/[), ]//g')
sed "6 s/.*/    \"version\": ($version0, $version1, $(($version2+1))),/" $input > ./temp.py
mv ./temp.py ./__init__.py