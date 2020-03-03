#!/bin/bash
input="/builds/real2u/blender2u/__init__.py"
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

version="$version0.$version1.$version2"

curl -X POST --silent --show-error --fail \
  "https://gitlab.my.org/api/v4/projects/16221229/repository/tags?tag_name=${version}&private_token=${GITLAB_TOKEN}"