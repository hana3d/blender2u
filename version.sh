#!/bin/bash
input="./__init__.py"
version=`sed "6q;d" $input`
# echo $((${version:22:1}+1))
sed "6 s/.*/    \"version\": (1, 4, $((${version:22:1}+1))),/" $input > ./temp.py
mv ./temp.py ./__init__.py