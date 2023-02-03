#!/bin/bash

if [ $# -eq 1 ]; then
  file_path=$1
else
  echo -n "modoverrides.lua路径: "
  read file_path
fi

content=$(cat $file_path)

numbers=$(echo "$content" | sed -n 's/^.*"workshop-\([0-9]\+\)".*$/\1/p')
echo "检测到以下MOD: "

output=""
for number in $numbers; do
  echo $number
  output+="ServerModSetup(\"$number\")\n"
done

echo -n "是否输出'dedicated_server_mods_setup.lua' (yes/no)? "
read write_file
if [ "$write_file" == "yes" ]; then
  echo -e "$output" > dedicated_server_mods_setup.lua
  echo "已输出到dedicated_server_mods_setup.lua"
fi
