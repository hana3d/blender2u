#!/bin/bash
input="./__init__.py"
line=`sed "6q;d" $input`

tmp="${line%%(*}"
if [ "$tmp" != "$line" ]; then
  line=$(echo "${line:$((${#tmp}+1))}")
fi
tmp="${line%%,*}"
if [ "$tmp" != "$line" ]; then
  version0=$(echo "${line:0:$((${#tmp}))}")
  line=$(echo "${line:$((${#tmp}+2))}")
fi
tmp="${line%%,*}"
if [ "$tmp" != "$line" ]; then
  version1=$(echo "${line:0:$((${#tmp}))}")
  line=$(echo "${line:$((${#tmp}+2))}")
fi
tmp="${line%%)*}"
if [ "$tmp" != "$line" ]; then
  version2=$(echo "${line:0:$((${#tmp}))}")
fi

sed "6 s/.*/    \"version\": ($version0, $version1, $(($version2+1))),/" $input > ./temp.py
mv ./temp.py ./__init__.py