#!/bin/bash
input="./__init__.py"
version=`sed "6q;d" $input`
version=$(echo "${version:22:3}" | sed 's/[), ]//g')
sed "6 s/.*/    \"version\": (1, 4, $(($version+1))),/" $input > ./temp.py
mv ./temp.py ./__init__.py